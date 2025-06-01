from django.db import connection
# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users.authentication import JWTAuthentication
from django.http import JsonResponse
from django.shortcuts import render
# from django.views import View
from rest_framework.views import APIView

from users.utils import write_to_rtdb, get_from_rtdb, update_rtdb, delete_from_rtdb
from django.contrib.auth import get_user_model
User = get_user_model()




class ViewAllFruits(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """ get all fruits in database """
        query = "SELECT * FROM fruits"

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        fruits = []
        for row in rows:
            fruit = {
                'id': row[0],
                'name': row[1],
                'botanical_name': row[2],
                'vitamin': row[3],
                'benefits': row[4],
                'side_effects': row[5],
                'ph': row[6],
                'preservative_methods': row[7]
            }
            fruits.append(fruit)

        return JsonResponse(fruits, safe=False)


class FruitSearchView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Retrieve search parameters from query string
        fruit_name = request.GET.get('name', '')
        fruit_vitamin = request.GET.get('vitamin', '')
        fruit_botanic = request.GET.get('botanic', '')

        # Prepare the SQL query
        query = "SELECT * FROM fruits WHERE"
        params = []

        if not (fruit_name or fruit_botanic or fruit_vitamin):
            return Response(data={'message': 'Bad search parameter. Use either name, vitamin or botanic'}, status=status.HTTP_400_BAD_REQUEST)
        if fruit_name:
            query += " fruits LIKE %s"
            params.append(fruit_name + '%')

        if fruit_vitamin:
            query += " type_of_vitamin LIKE %s"
            params.append(fruit_vitamin + '%')

        if fruit_botanic:
            query += " botanical_name LIKE %s"
            params.append(fruit_botanic + '%')

        # Execute the SQL query
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        fruits = []
        for row in rows:
            fruit = {
                'id': row[0],
                'name': row[1],
                'botanical_name': row[2],
                'vitamin': row[3],
                'benefits': row[4],
                'side_effects': row[5],
                'ph': row[6],
                'preservative_methods': row[7]
            }
            fruits.append(fruit)

        return JsonResponse(fruits, safe=False)

class UserFruitFavoritesView(APIView):
    """
    Manage user's favorite fruits in Firebase Realtime Database.
    Data is stored under `user_favorites/<user_id>/<fruit_id>: true/false`.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get all favorite fruit IDs for the authenticated user.
        """
        user_id = str(request.user.id)
        rtdb_path = f'user_favorites/{user_id}'

        try:
            favorites = get_from_rtdb(rtdb_path)
            # RTDB returns None if path doesn't exist, or a dict of favorites
            if favorites:
                # Filter for fruits marked as true (favorited)
                favorited_fruit_ids = [k for k, v in favorites.items() if v is True]
                return Response({"favorite_fruit_ids": favorited_fruit_ids}, status=status.HTTP_200_OK)
            return Response({"favorite_fruit_ids": []}, status=status.HTTP_200_OK) # Return empty list if no favorites
        except Exception as e:
            return Response({"error": f"Error retrieving favorites: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Add a fruit to the user's favorites.
        Requires 'fruit_id' in request body.
        """
        user_id = str(request.user.id)
        fruit_id = request.data.get('fruit_id')

        if not fruit_id:
            return Response({"error": "fruit_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Optional: Validate if fruit_id actually exists in your Django database
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM fruits WHERE id = %s", [fruit_id])
                if cursor.fetchone()[0] == 0:
                    return Response({"error": "Fruit with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Database validation error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rtdb_path = f'user_favorites/{user_id}/{fruit_id}'

        try:
            # Set a boolean flag in RTDB to indicate favorited
            write_to_rtdb(rtdb_path, True)
            return Response({"message": f"Fruit {fruit_id} added to favorites."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error adding to favorites: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """
        Remove a fruit from the user's favorites.
        Requires 'fruit_id' in request body.
        """
        user_id = str(request.user.id)
        fruit_id = request.data.get('fruit_id')

        if not fruit_id:
            return Response({"error": "fruit_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        rtdb_path = f'user_favorites/{user_id}/{fruit_id}'

        try:
            # Delete the specific fruit entry
            delete_from_rtdb(rtdb_path)
            return Response({"message": f"Fruit {fruit_id} removed from favorites."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error removing from favorites: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
