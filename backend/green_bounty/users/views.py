# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .authentication import JWTAuthentication
from .models import User
from .serializers import (ChangePasswordSerializer, LoginSerializer,
                          RegisterSerializer, UpdateUserSerializer,
                          UserSerializer)
from .validations import clean_data, tidy_data

# Create your views here.

# helper

from .utils import write_to_rtdb, get_from_rtdb, update_rtdb, delete_from_rtdb

class UserRealtimeDataView(APIView):
    """
    API view to manage user-specific data in Firebase Realtime Database.
    Requires a valid JWT token for authentication.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retrieve data for the authenticated user from RTDB.
        Data will be stored under 'users/<user_id>/data'.
        """
        user_id = str(request.user.id) # Use the Django user's ID as part of the RTDB path
        rtdb_path = f'users/{user_id}/data'

        try:
            data = get_from_rtdb(rtdb_path)
            if data:
                return Response(data, status=status.HTTP_200_OK)
            return Response({"message": "No data found for this user in Realtime Database"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error retrieving data from RTDB: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create/overwrite data for the authenticated user in RTDB.
        """
        user_id = str(request.user.id)
        rtdb_path = f'users/{user_id}/data'
        data_to_store = request.data

        if not isinstance(data_to_store, dict):
            return Response({"error": "Request data must be a JSON object."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            write_to_rtdb(rtdb_path, data_to_store)
            return Response({"message": "Data written to Realtime Database successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Error writing data to RTDB: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        """
        Update (merge) data for the authenticated user in RTDB.
        """
        user_id = str(request.user.id)
        rtdb_path = f'users/{user_id}/data'
        data_to_update = request.data

        if not isinstance(data_to_update, dict):
            return Response({"error": "Request data for update must be a JSON object."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_rtdb(rtdb_path, data_to_update)
            return Response({"message": "Data updated in Realtime Database successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error updating data in RTDB: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        Delete data for the authenticated user from RTDB.
        """
        user_id = str(request.user.id)
        rtdb_path = f'users/{user_id}/data'

        try:
            delete_from_rtdb(rtdb_path)
            return Response({"message": "Data deleted from Realtime Database successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Error deleting data from RTDB: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def get_token(self, request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)

    return token


class WelcomeView(generics.GenericAPIView):
    """ returns welcome message """
    permission_classes = [permissions.AllowAny]
    ##

    def get(self, request):
        return Response({'message': "GreenBounty API - Fueling Your App with Nature's Harvest"}, status=status.HTTP_200_OK)


class UserListApiView(generics.ListCreateAPIView):
    """ filter api for admins """
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'email'

    search_fields = (
        '^email',
    )


class UserRegister(generics.GenericAPIView):
    """ register api view """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        """ User sign up"""
        # print(f"Request data ==> {request.data}")
        data = clean_data(request.data)
        # print(f"Clean data ==> {data}")
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(data)
            if user:
                login(request, user)

                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                return Response({'token': token})
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(generics.GenericAPIView):
    """
    Logs in an existing user.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """
        Checks if user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validate(data)
            login(request, user)
            token = get_token(self, request)
            usr = UserSerializer(request.user)
            msg = tidy_data(usr.data, token)
            return Response(msg, status=status.HTTP_200_OK)


class UserLogout(APIView):
    """ logout user """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        msg = {'message': 'Logged Out Successfully'}
        return Response(data=msg, status=status.HTTP_200_OK)


class UserView(generics.GenericAPIView):
    """ User view """
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        # notify = NotificationSerializer(request.user)
        return Response({
            'user': serializer.data,
        }, status=status.HTTP_200_OK)


class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializer
    # lookup_field = 'email'


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangePasswordSerializer


class DeleteUserView(generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, pk=None):
        Usr = User.objects.filter(pk=pk)
        Usr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
