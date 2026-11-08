from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView



urlpatterns=[
    path('register/',views.RegisterView.as_view(),name='register'),
    path('me/',views.UserView.as_view(),name='user-detail'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh')
]