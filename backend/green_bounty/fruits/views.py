from django.db import connection
# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users.authentication import JWTAuthentication
from django.http import JsonResponse
from django.shortcuts import render
# from django.views import View


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
