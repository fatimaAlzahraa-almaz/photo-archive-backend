from rest_framework import serializers
from .models import Photo,PhotoMetadata

class PhotoListSerializer(serializers.ModelSerializer):
    taken_at=serializers.DateTimeField(source='metadata.taken_at',read_only=True ,allow_null=True,
    default=None)
    display_date=serializers.SerializerMethodField()
    class Meta:
        model=Photo
        fields=['id','thumbnail','created_at','taken_at','display_date']
    def get_display_date(self, obj):
       metadata = getattr(obj, 'metadata', None)

       if metadata and metadata.taken_at:
           return metadata.taken_at

       return obj.created_at
   

class PhotoMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model=PhotoMetadata
        fields=['id','photo','taken_at','camera_make','camera_model','longitude','latitude','raw_metadata']
        
class PhotoDetailsSerializer(serializers.ModelSerializer):
    metadata=PhotoMetadataSerializer(read_only=True)
    class Meta:
        model=Photo
        fields=['id','name','image','thumbnail','size','width','height','created_at','metadata']
        
class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Photo
        fields=['id','name','image','size','width','height','thumbnail','created_at']
        read_only_fields=['id','thumbnail','created_at','size','width','height','name']