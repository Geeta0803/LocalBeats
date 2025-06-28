from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='tracks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    likes=models.ManyToManyField(User, related_name='liked_tracks',blank=True)
