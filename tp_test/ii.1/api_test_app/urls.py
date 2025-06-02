from django.urls import path
from .views import AlbumListApiView, AlbumDetailApiView

urlpatterns = [
    path('api/albums/', AlbumListApiView.as_view(), name='album-list-api'),
    path('api/albums/<int:pk>/', AlbumDetailApiView.as_view(), name='album-detail-api'),
]
