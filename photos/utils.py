
import math
import struct
from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, ExifTags

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone



def clean_exif_text(value):
    """Convert EXIF text values into clean strings."""

    if value is None:
        return ''

    if isinstance(value, bytes):
        value = value.decode('utf-8', errors='replace')

    return str(value).replace('\x00', '').strip()


def to_json_safe(value):

    if value is None or isinstance(value, (int, bool)):
        return value

    if isinstance(value, str):
        return value.replace('\x00', '')

    if isinstance(value, float):
        return value if math.isfinite(value) else None

    if isinstance(value, (bytes, bytearray)):
        try:
            return bytes(value).decode(
                'utf-8',
                errors='replace'
            ).replace('\x00', '')

        except UnicodeDecodeError:
            return bytes(value).hex()

    if isinstance(value, (tuple, list)):
        return [
            to_json_safe(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            str(key).replace('\x00', ''): to_json_safe(val)
            for key, val in value.items()
        }

    try:
        number = float(value)
        return number if math.isfinite(number) else None

    except (TypeError, ValueError, OverflowError):
        return str(value).replace('\x00', '')
    

def convert_ifd_to_dict(ifd, tag_names):
    """Convert EXIF IFD numeric tags into readable names."""

    result = {}

    for tag_id, value in ifd.items():

        # Skip vendor-specific binary metadata
        if tag_id == 37500:  # MakerNote
            continue

        tag_name = tag_names.get(tag_id, str(tag_id))

        result[tag_name] = to_json_safe(value)

    return result


def get_ifd_safely(exif, ifd_tag):
    """Read a nested EXIF IFD without failing on malformed metadata."""

    try:
        return exif.get_ifd(ifd_tag)

    except (
        AttributeError,
        KeyError,
        TypeError,
        ValueError,
        OSError,
        SyntaxError,
        IndexError,
        struct.error,
        OverflowError
    ):
        return {}


def gps_to_decimal(
    coordinate,
    reference,
    positive_ref,
    negative_ref,
    max_value
):
    """Convert GPS degrees, minutes and seconds into decimal degrees."""

    try:
        if len(coordinate) != 3:
            return None

        degrees, minutes, seconds = map(float, coordinate)

        if not all(math.isfinite(v) for v in (
            degrees, minutes, seconds
        )):
            return None

        if not 0 <= degrees <= max_value:
            return None

        if not 0 <= minutes < 60:
            return None

        if not 0 <= seconds < 60:
            return None

        if degrees == max_value and (minutes or seconds):
            return None

        decimal = degrees + minutes / 60 + seconds / 3600

        reference = clean_exif_text(reference).upper()

        if reference == negative_ref:
            decimal = -decimal

        elif reference != positive_ref:
            return None

        return decimal

    except (
        TypeError,
        ValueError,
        OverflowError,
        ZeroDivisionError
    ):
        return None


def parse_exif_datetime(value, offset=None):
    """Parse EXIF datetime and apply its timezone offset when available."""

    value = clean_exif_text(value)

    if not value:
        return None

    try:
        date = datetime.strptime(
            value,
            '%Y:%m:%d %H:%M:%S'
        )

    except ValueError:
        return None

    offset = clean_exif_text(offset)

    if offset:
        try:
            aware_date = datetime.fromisoformat(
                date.isoformat() + offset
            )

            if settings.USE_TZ:
                return aware_date

            return aware_date.replace(tzinfo=None)

        except ValueError:
            pass

    
    if settings.USE_TZ:
        return timezone.make_aware(
            date,
            timezone.get_default_timezone()
        )

    return date



def extract_img_info(image):
    

    image.seek(0)

    try:
        name = Path(image.name).name
        size = image.size

        with Image.open(image) as source:

            oriented = ImageOps.exif_transpose(source)

            try:
                width, height = oriented.size

            finally:
                oriented.close()

        return {
            'name': name,
            'size': size,
            'width': width,
            'height': height
        }

    finally:
        image.seek(0)



def create_thumbnail(image, size=(400, 400), quality=85):
    """Generate a JPEG thumbnail while preserving aspect ratio."""

    image.seek(0)
    output = BytesIO()

    try:
        with Image.open(image) as source:

            
            img = ImageOps.exif_transpose(source)

            try:
                
                img.thumbnail(
                    size,
                    Image.Resampling.LANCZOS
                )

                
                has_alpha = (
                    'A' in img.getbands()
                    or 'transparency' in img.info
                )

                if has_alpha:
                    rgba = img.convert('RGBA')

                    background = Image.new(
                        'RGBA',
                        rgba.size,
                        (255, 255, 255, 255)
                    )

                    try:
                        rgb = Image.alpha_composite(
                            background,
                            rgba
                        ).convert('RGB')

                    finally:
                        rgba.close()
                        background.close()

                else:
                    rgb = img.convert('RGB')

                try:
                    
                    rgb.save(
                        output,
                        format='JPEG',
                        quality=quality,
                        optimize=True
                    )

                finally:
                    rgb.close()

            finally:
                img.close()

        filename = (
            f'{Path(image.name).stem}_thumbnail.jpg'
        )

        return ContentFile(
            output.getvalue(),
            name=filename
        )

    finally:
        output.close()
        image.seek(0)



def extract_metadata(image):
    """Extract camera, capture date, GPS and raw EXIF metadata."""

    image.seek(0)

    metadata = {
        'taken_at': None,
        'camera_make': '',
        'camera_model': '',
        'longitude': None,
        'latitude': None,
        'raw_metadata': {}
    }

    try:
        with Image.open(image) as img:

            try:
                exif = img.getexif()

            except (
                OSError,
                ValueError,
                SyntaxError,
                TypeError,
                struct.error
            ):
                return metadata

            
            if not exif:
                return metadata

            
            exif_ifd = get_ifd_safely(
                exif,
                ExifTags.IFD.Exif
            )

            gps_ifd = get_ifd_safely(
                exif,
                ExifTags.IFD.GPSInfo
            )

           
            metadata['camera_make'] = clean_exif_text(
                exif.get(271)
            )

            metadata['camera_model'] = clean_exif_text(
                exif.get(272)
            )

            
            metadata['taken_at'] = parse_exif_datetime(
                exif_ifd.get(0x9003),
                exif_ifd.get(0x9011)
            )

            
            if metadata['taken_at'] is None:

                metadata['taken_at'] = parse_exif_datetime(
                    exif_ifd.get(0x9004),
                    exif_ifd.get(0x9012)
                )

            

            metadata['latitude'] = gps_to_decimal(
                gps_ifd.get(2),
                gps_ifd.get(1),
                'N',
                'S',
                90
            )

            metadata['longitude'] = gps_to_decimal(
                gps_ifd.get(4),
                gps_ifd.get(3),
                'E',
                'W',
                180
            )

            
            exif_tags = (
                ExifTags.IFD.Exif,
                ExifTags.IFD.GPSInfo
            )

            main_ifd = {
                tag_id: value
                for tag_id, value in exif.items()
                if tag_id not in exif_tags
            }

            raw_metadata = {}

            if main_ifd:
                raw_metadata['image'] = convert_ifd_to_dict(
                    main_ifd,
                    ExifTags.TAGS
                )

            if exif_ifd:
                raw_metadata['exif'] = convert_ifd_to_dict(
                    exif_ifd,
                    ExifTags.TAGS
                )

            if gps_ifd:
                raw_metadata['gps'] = convert_ifd_to_dict(
                    gps_ifd,
                    ExifTags.GPSTAGS
                )

            metadata['raw_metadata'] = raw_metadata

            return metadata

    finally:
        image.seek(0)
