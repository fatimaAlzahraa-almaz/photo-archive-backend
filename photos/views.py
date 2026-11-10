from .serializers import PhotoListSerializer,PhotoDetailsSerializer,PhotoUploadSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Photo
from .services import create_photo
# Create your views here.

class PhotoDetailsView(generics.RetrieveDestroyAPIView):
    serializer_class=PhotoDetailsSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user).select_related('metadata')
      
class PhotoListCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user).select_related('metadata')
    def get_serializer_class(self):
        if self.request.method=='POST':
            return PhotoUploadSerializer
        return PhotoListSerializer
    def perform_create(self, serializer):
        image=serializer.validated_data['image']
        photo=create_photo(image=image,user=self.request.user)
        serializer.instance=photo
