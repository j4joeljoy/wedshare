from django.contrib import admin
from .models import Photo, PhotoView, PhotoLike, PhotoComment, PhotoDownload

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at')
    search_fields = ('title',)

@admin.register(PhotoView)
class PhotoViewAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user', 'viewed_at')

@admin.register(PhotoLike)
class PhotoLikeAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user', 'liked_at')

@admin.register(PhotoComment)
class PhotoCommentAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user', 'comment', 'commented_at')

@admin.register(PhotoDownload)
class PhotoDownloadAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user', 'downloaded_at')
