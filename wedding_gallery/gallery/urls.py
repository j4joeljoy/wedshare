from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_home, name='home'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('like/<int:photo_id>/', views.like_photo, name='like_photo'),
    path('download/<int:photo_id>/', views.download_photo, name='download_photo'),
    path('download-all/', views.download_all_photos, name='download_all'),
]
