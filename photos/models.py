from django.db import models
from django.conf import settings
# Create your models here.

class Photo(models.Model):
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='photos/')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='photos')
    thumbnail=models.ImageField(upload_to='thumbnails/', blank=True,null=True)
    size=models.PositiveIntegerField()
    width=models.PositiveIntegerField()
    height=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.name

class PhotoMetadata(models.Model):
    photo=models.OneToOneField(Photo,on_delete=models.CASCADE,related_name='metadata')
    camera_make=models.CharField(max_length=100,blank=True,null=True)
    camera_model=models.CharField(max_length=100,blank=True,null=True)
    taken_at=models.DateTimeField(blank=True,null=True)
    longitude=models.FloatField(blank=True,null=True)
    latitude=models.FloatField(blank=True,null=True)
    raw_metadata=models.JSONField(default=dict,blank=True)

    def __str__(self):
        return f'Metadata for {self.photo.name}'

