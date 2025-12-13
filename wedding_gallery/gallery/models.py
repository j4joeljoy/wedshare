from django.db import models
from django.contrib.auth.models import User
from accounts.models import GuestUser

class Photo(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image_url = models.URLField()  # Cloud storage URL
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Photo"

class PhotoView(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(GuestUser, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

class PhotoLike(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(GuestUser, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('photo', 'user')

class PhotoComment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(GuestUser, on_delete=models.CASCADE)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

class PhotoDownload(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(GuestUser, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)
