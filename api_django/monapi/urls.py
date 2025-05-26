from django.urls import path
from .views import CommentaireListApiView, CommentaireDetailApiView
urlpatterns = [
    path('api/', CommentaireListApiView.as_view(), name='commentaire-list-api'),
    path('api/<int:pk>/', CommentaireDetailApiView.as_view(), name='commentaire-detail-api'),
]


