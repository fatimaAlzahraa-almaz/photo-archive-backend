from .utils import extract_metadata,extract_img_info,create_thumbnail
from .models import Photo,PhotoMetadata
from django.db import transaction

@transaction.atomic
def create_photo(image,user):
    image.seek(0)
    metadata=extract_metadata(image)
    image.seek(0)
    image_info=extract_img_info(image)
    image.seek(0)
    thumbnail=create_thumbnail(image)
    image.seek(0)
    photo=Photo.objects.create(image=image,user=user,thumbnail=thumbnail,**image_info)
    PhotoMetadata.objects.create(photo=photo,**metadata)
    return photo