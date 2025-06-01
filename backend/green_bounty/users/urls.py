# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('user/', views.UserView.as_view(), name='user'),
    path('filter/', views.UserListApiView.as_view(), name='filter'),
    path('update_profile/<int:pk>/',
         views.UpdateProfileView.as_view(), name='update_profile'),
    path('change_password/<int:pk>/',
         views.ChangePasswordView.as_view(), name='change_password'),
    path('delete_user/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),
    path('user-rtdb/', views.UserRealtimeDataView.as_view(), name='user-rtdb'),
]
