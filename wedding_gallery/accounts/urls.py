from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('guest/login/', views.guest_login, name='guest_login'),
    path('photographer/login/', views.photographer_login, name='photographer_login'),
    path('photographer/logout/', views.photographer_logout, name='photographer_logout'),
]
