# Create your views here.
from django.contrib.auth import login, logout
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (ChangePasswordSerializer, LoginSerializer,
                          RegisterSerializer,
                          UpdateUserSerializer, UserSerializer)
from .validations import clean_data

# Create your views here.


class WelcomeView(generics.GenericAPIView):
    """ returns welcome message """
    permission_classes = (permissions.AllowAny,)
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
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """ User sign up"""
        # print(f"Request data ==> {request.data}")
        data = clean_data(request.data)
        # print(f"Clean data ==> {data}")
        serializer = self.serializer_class(data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(generics.GenericAPIView):
    """
    Logs in an existing user.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    authentication_classes = (SessionAuthentication,)

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
            usr = UserSerializer(request.user)
            return Response(usr.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    """ logout user """
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(generics.GenericAPIView):
    """ User view """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication, )

    def get(self, request):
        serializer = UserSerializer(request.user)
        # notify = NotificationSerializer(request.user)
        return Response({
            'user': serializer.data,
        }, status=status.HTTP_200_OK)


class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    authentication_classes = (SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UpdateUserSerializer
    # lookup_field = 'email'


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class DeleteUserView(generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    def delete(self, request, pk=None):
        Usr = User.objects.filter(pk=pk)
        Usr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
