from django.contrib import admin
from .models import Photo,PhotoMetadata
# Register your models here.

admin.site.register(Photo)
admin.site.register(PhotoMetadata)
