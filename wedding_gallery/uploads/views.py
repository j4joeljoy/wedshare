from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import cloudinary.uploader
from gallery.models import Photo
from .forms import PhotoUploadForm

from django.contrib import messages

@login_required(login_url='accounts:photographer_login')
def upload_photo(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            
            # Upload to Cloudinary with folder and watermark
            image_file = request.FILES['image_file']
            try:
                result = cloudinary.uploader.upload(
                    image_file,
                    folder="wedding_gallery",
                    transformation=[
                        {
                            'overlay': 'text:Arial_30:Wedding Memories',
                            'gravity': 'south_east',
                            'opacity': 50,
                            'color': 'white'
                        }
                    ]
                )
                photo.image_url = result['secure_url']
                photo.save()
                messages.success(request, "Photo uploaded successfully!")
                return redirect('uploads:dashboard')
            except Exception as e:
                # Handle upload error
                print(f"Upload error: {e}")
                messages.error(request, f"Upload failed: {e}")
    else:
        form = PhotoUploadForm()

    return render(request, 'uploads/upload.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from gallery.models import (
    Photo, PhotoView, PhotoLike, PhotoComment, PhotoDownload
)

@login_required(login_url='accounts:photographer_login')
def photographer_dashboard(request):
    photos = Photo.objects.filter(uploaded_by=request.user)

    stats = {
        'total_photos': photos.count(),
        'views': PhotoView.objects.filter(photo__in=photos).count(),
        'likes': PhotoLike.objects.filter(photo__in=photos).count(),
        'comments': PhotoComment.objects.filter(photo__in=photos).count(),
        'downloads': PhotoDownload.objects.filter(photo__in=photos).count(),
    }

    photo_stats = photos.annotate(
        views=Count('photoview'),
        likes=Count('photolike'),
        comments=Count('photocomment'),
        downloads=Count('photodownload')
    )

    # Recent Downloads of my photos
    recent_downloads = PhotoDownload.objects.filter(photo__in=photos).select_related('user', 'photo').order_by('-downloaded_at')[:20]

    return render(request, 'uploads/dashboard.html', {
        'stats': stats,
        'photos': photo_stats,
        'recent_downloads': recent_downloads
    })

@login_required(login_url='accounts:photographer_login')
def delete_photo(request, photo_id):
    if request.method == "POST":
        photo = get_object_or_404(Photo, id=photo_id)
        
        # Ensure only the uploader or admin can delete
        if photo.uploaded_by == request.user or request.user.is_staff:
            # Optional: Delete from Cloudinary as well
            # if photo.image_url:
            #     public_id = ... # Extract public_id from URL
            #     cloudinary.uploader.destroy(public_id)
            
            photo.delete()
            messages.success(request, "Photo deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete this photo.")
            
    return redirect('uploads:dashboard')

