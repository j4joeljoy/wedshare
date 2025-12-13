from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from accounts.models import GuestUser
from gallery.models import Photo, PhotoView, PhotoLike, PhotoComment, PhotoDownload
from .models import PageView

@staff_member_required
def admin_dashboard(request):
    stats = {
        'total_guests': GuestUser.objects.count(),
        'total_photos': Photo.objects.count(),
        'total_page_views': PageView.objects.count(),
        'total_photo_views': PhotoView.objects.count(),
        'total_likes': PhotoLike.objects.count(),
        'total_comments': PhotoComment.objects.count(),
        'total_downloads': PhotoDownload.objects.count(),
    }

    # Recent Activity (e.g., last 10 page views)
    recent_activity = PageView.objects.order_by('-viewed_at')[:10]
    
    # Recent Guests
    recent_guests = GuestUser.objects.order_by('-created_at')[:10]

    # All Photos for Admin Review
    photos = Photo.objects.annotate(
        views=Count('photoview'),
        likes=Count('photolike')
    ).order_by('-uploaded_at')

    # Recent Downloads
    recent_downloads = PhotoDownload.objects.select_related('user', 'photo').order_by('-downloaded_at')[:20]

    # Daily Page Views for Graph
    from django.db.models.functions import TruncDate
    from django.utils import timezone
    from datetime import timedelta
    
    # Get last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_views = PageView.objects.filter(viewed_at__gte=thirty_days_ago)\
        .annotate(date=TruncDate('viewed_at'))\
        .values('date')\
        .annotate(count=Count('id'))\
        .order_by('date')
    
    daily_views_data = {
        'dates': [dv['date'].strftime('%Y-%m-%d') for dv in daily_views],
        'counts': [dv['count'] for dv in daily_views]
    }

    return render(request, 'dashboard/admin_dashboard.html', {
        'stats': stats,
        'recent_activity': recent_activity,
        'recent_guests': recent_guests,
        'photos': photos,
        'recent_downloads': recent_downloads,
        'daily_views_data': daily_views_data
    })
