from django.urls import path
from . import views

app_name = 'uploads'

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo'),
    path('dashboard/', views.photographer_dashboard, name='dashboard'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
]
