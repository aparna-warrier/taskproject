from django.db import models

class ShortURL(models.Model):
    original_url = models.URLField(max_length=1000)
    short_code   = models.CharField(max_length=20, unique=True, db_index=True)
    clicks       = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"


# Create your models here.
