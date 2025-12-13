from django.shortcuts import render
from gallery.models import Photo

def landing_page(request):
    # Fetch recent photos for the carousel (e.g., last 10 for the 3D effect)
    carousel_photos = Photo.objects.all().order_by('-uploaded_at')[:10]
    
    # Fetch photos for the scattered grid (skip the first 10 to avoid duplicates if possible, or just take random ones)
    # For simplicity, we'll take the next 8
    scattered_photos = Photo.objects.all().order_by('-uploaded_at')[10:18]
    if not scattered_photos:
        # Fallback if not enough photos, just reuse some
        scattered_photos = Photo.objects.all().order_by('?')[:8]
    # For now, we'll just take the next 4, or reuse carousel ones if not enough
    card_photos = Photo.objects.all().order_by('?')[:4]

    return render(request, 'landing.html', {
        'carousel_photos': carousel_photos,
        'card_photos': card_photos
    })
