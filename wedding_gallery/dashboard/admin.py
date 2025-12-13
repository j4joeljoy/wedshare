from django.contrib import admin
from .models import PageView

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('page', 'ip_address', 'viewed_at')
    list_filter = ('page',)
