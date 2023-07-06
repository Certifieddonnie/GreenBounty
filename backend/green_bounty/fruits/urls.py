# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('fruits', views.ViewAllFruits.as_view(), name='all_fruits'),
    path('fruits/search/', views.FruitSearchView.as_view(), name='fruit_search'),

]
