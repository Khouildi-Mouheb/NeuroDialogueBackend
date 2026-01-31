from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home,CustomLoginView , CustomLogoutView , profile, register


urlpatterns=[
    path('',home, name='home'),
    path('users/register/', register, name='register'),
    path('users/logout/',CustomLogoutView.as_view(),name='logout'),
    path('users/login/',CustomLoginView.as_view(),name='login'),
    path('users/login/',CustomLoginView.as_view(),name='login'),
    path('users/profile/<str:user_id>/',profile,name='profile'),
    
]


