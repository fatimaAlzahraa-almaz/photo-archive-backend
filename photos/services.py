import logging
from django.db import transaction

from .utils import (
    extract_metadata,
    extract_img_info,
    create_thumbnail
)

from .models import Photo, PhotoMetadata


logger = logging.getLogger(__name__)


def create_photo(image, user):

    metadata = extract_metadata(image)
    image_info = extract_img_info(image)
    thumbnail = create_thumbnail(image)

    
    saved_files = []

    photo = Photo(
        user=user,
        **image_info
    )

    try:
        with transaction.atomic():

            
            image.seek(0)
            photo.image.save(
                image.name,
                image,
                save=False
            )

            saved_files.append((
                photo.image.storage,
                photo.image.name
            ))

            
            thumbnail.seek(0)
            photo.thumbnail.save(
                thumbnail.name,
                thumbnail,
                save=False
            )

            saved_files.append((
                photo.thumbnail.storage,
                photo.thumbnail.name
            ))

            
            photo.save()

            
            PhotoMetadata.objects.create(
                photo=photo,
                **metadata
            )

        return photo

    except Exception:

        
        for storage, filename in reversed(saved_files):
            try:
                storage.delete(filename)

            except Exception:
                logger.exception(
                    "Failed to delete uploaded file: %s",
                    filename
                )

        raise
    
    
    
    


logger = logging.getLogger(__name__)


def delete_stored_files(files):
    for storage, name in files:
        try:
            storage.delete(name)

        except Exception:
            logger.exception(
                "Failed to delete file: %s",
                name
            )


def delete_photo(photo):

    
    files = []

    for field_name in ('image', 'thumbnail'):
        file_field = getattr(photo, field_name)

        if file_field and file_field.name:
            files.append((
                file_field.storage,
                file_field.name
            ))

    with transaction.atomic():

        
        photo.delete()

        
        transaction.on_commit(
            lambda: delete_stored_files(files)
        )