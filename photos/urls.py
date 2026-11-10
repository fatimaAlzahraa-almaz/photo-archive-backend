from django.urls import path
from . import views


urlpatterns = [
  path('',views.PhotoListCreateView.as_view(),name='photo-list-create'),
  path('<int:pk>/',views.PhotoDetailsView.as_view(),name='photo-details'),
]