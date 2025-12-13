from django.db import models

class PageView(models.Model):
    page = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.page
