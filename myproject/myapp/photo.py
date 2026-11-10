from PIL import Image
import os
from io import BytesIO
from django.core.files.baseimport ContentFile
def creat_thumbnail(image_file , size=(500,500)):
  img=Image.open(image_file)
    
  if img.mode in ("RGBA","p"):
      img=img.convert("RGB")
  img.thumbnail(size)
  thumb_io = BytesIO()
  img.save(thumb_io,format='JPEG',quality=85)
  thumb_io.seek(0)
  file_name=os.path.basename(image_file.name)
  name_only,_ = os.path.splitext(file_name)
  thumbnail_name=f"{name_only}_thumb.jpg"
  thumbnail_file = ContentFile(thumb_io.read(),name=thumbnail_name)
  return thumbnail_file