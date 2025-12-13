from .models import PageView

class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Track views for gallery pages, excluding admin and static
        if request.path.startswith('/gallery') and not request.path.startswith('/admin') and not request.path.startswith('/static'):
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            PageView.objects.create(
                page=request.path,
                ip_address=ip
            )
        return response
