from django.db import models
from django.conf import settings
# Create your models here.


class Album(models.Model):
    name=models.CharField(max_length=255)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='albums')
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created_at']
    def __str__(self):
        return self.name
      
class AlbumPhoto(models.Model):
    album=models.ForeignKey(Album,on_delete=models.CASCADE,related_name='album_photos')
    photo=models.ForeignKey('photos.Photo',on_delete=models.CASCADE,related_name='photo_albums')
    added_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album', 'photo'],
                name='unique_album_photo'
            )
        ]
        ordering = ['-added_at']
    def __str__(self):
        return f'{self.photo.name} in {self.album.name}'