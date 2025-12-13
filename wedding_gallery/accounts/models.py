from django.db import models
from django.contrib.auth.models import User


class GuestUser(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    cookies_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # auto-generate username and name from email
        if not self.username:
            self.username = self.email.split('@')[0]
        if not self.name:
            self.name = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
