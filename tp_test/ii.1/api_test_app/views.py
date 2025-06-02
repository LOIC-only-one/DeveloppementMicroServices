from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Album
from .serializer import AlbumSerializer

# Create your views here.

class AlbumListApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Récupérer tous les albums, avec filtrage optionnel par titre.
        """
        titre = request.query_params.get('titre')
        if titre is not None:
            albums = Album.objects.filter(titre=titre)
        else:
            albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, 200)

    def post(self, request, *args, **kwargs):
        """
        Créer un nouvel album.
        """
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)


class AlbumDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        """
        Récupérer un album par son id.
        """
        album = self.get_object(pk)
        if not album:
            return Response({"erreur": "album non trouvé"}, 404)
        serializer = AlbumSerializer(album)
        return Response(serializer.data, 200)

    def put(self, request, pk, *args, **kwargs):
        """
        Mettre à jour un album (total ou partiel).
        """
        album = self.get_object(pk)
        if not album:
            return Response({"erreur": "album non trouvé"}, 404)
        serializer = AlbumSerializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response(serializer.errors, 400)

    def delete(self, request, pk, *args, **kwargs):
        """
        Supprimer un album.
        """
        album = self.get_object(pk)
        if not album:
            return Response({"erreur": "album non trouvé"}, 404)
        album.delete()
        return Response({"message": "album supprimé avec succès"}, 204)
