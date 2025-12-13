from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Photo, PhotoView, PhotoLike, PhotoComment, PhotoDownload
from accounts.models import GuestUser
from .forms import CommentForm
import requests
import zipfile
import io

def get_guest(request):
    guest_id = request.session.get('guest_id')
    if not guest_id:
        return None
    return GuestUser.objects.filter(id=guest_id).first()

def gallery_home(request):
    guest = get_guest(request)
    if not guest:
        return redirect('accounts:guest_login')

    from django.db.models import Count
    photos = Photo.objects.annotate(
        views=Count('photoview'),
        likes=Count('photolike'),
        downloads=Count('photodownload')
    ).order_by('-uploaded_at')
    
    return render(request, 'gallery/home.html', {
        'photos': photos,
        'guest': guest
    })

def photo_detail(request, photo_id):
    guest = get_guest(request)
    if not guest:
        return redirect('accounts:guest_login')

    photo = get_object_or_404(Photo, id=photo_id)
    
    # Record View
    PhotoView.objects.get_or_create(photo=photo, user=guest)
    
    # Handle Comment
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.user = guest
            comment.save()
            return redirect('gallery:photo_detail', photo_id=photo.id)
    else:
        form = CommentForm()

    comments = PhotoComment.objects.filter(photo=photo).order_by('-commented_at')
    is_liked = PhotoLike.objects.filter(photo=photo, user=guest).exists()

    return render(request, 'gallery/photo_detail.html', {
        'photo': photo,
        'guest': guest,
        'form': form,
        'comments': comments,
        'is_liked': is_liked
    })

def like_photo(request, photo_id):
    guest = get_guest(request)
    if not guest:
        return redirect('accounts:guest_login')

    photo = get_object_or_404(Photo, id=photo_id)
    like, created = PhotoLike.objects.get_or_create(photo=photo, user=guest)
    if not created:
        like.delete() # Toggle like
        
    return redirect('gallery:photo_detail', photo_id=photo.id)

def download_photo(request, photo_id):
    guest = get_guest(request)
    if not guest:
        return redirect('accounts:guest_login')

    photo = get_object_or_404(Photo, id=photo_id)
    PhotoDownload.objects.create(photo=photo, user=guest)

    try:
        if photo.image_url.startswith('http'):
            img_data = requests.get(photo.image_url).content
        else:
            # Handle local file path if necessary, though image_url is URLField
            # Assuming it might be a relative URL for local media
            with open(photo.image_url.lstrip('/'), 'rb') as f:
                img_data = f.read()
    except Exception as e:
        raise Http404("Image not found")

    response = HttpResponse(img_data, content_type="image/jpeg")
    response['Content-Disposition'] = f'attachment; filename="photo_{photo.id}.jpg"'
    return response

def download_all_photos(request):
    guest = get_guest(request)
    if not guest:
        return redirect('accounts:guest_login')

    photos = Photo.objects.all()
    buffer = io.BytesIO()
    
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for photo in photos:
            try:
                if photo.image_url.startswith('http'):
                    img_data = requests.get(photo.image_url).content
                else:
                    with open(photo.image_url.lstrip('/'), 'rb') as f:
                        img_data = f.read()
                
                zip_file.writestr(f'photo_{photo.id}.jpg', img_data)
                PhotoDownload.objects.create(photo=photo, user=guest)
            except Exception:
                continue

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="wedding_photos.zip"'
    return response
