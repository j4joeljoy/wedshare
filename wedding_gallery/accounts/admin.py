from django.contrib import admin
from .models import GuestUser

@admin.register(GuestUser)
class GuestUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'cookies_accepted', 'created_at')
    search_fields = ('email', 'username')
