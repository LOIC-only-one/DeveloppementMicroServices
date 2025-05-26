from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Commentaire
from .serializer import CommentaireSerializer
from rest_framework import permissions


class CommentaireListApiView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve all comments.
        Returns a list of comments in JSON format.
        """
        commentaires = Commentaire.objects.all()
        id = request.query_params.get('id', None)
        serializer = CommentaireSerializer(commentaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            "titre": request.data.get("titre"),
            "comment": request.data.get("comment"),
        }

        serializer = CommentaireSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentaireDetailApiView(APIView):

    def get(self, request, pk, *args, **kwargs):
        """
        Handle GET requests to retrieve a specific comment by its ID.
        Returns the comment in JSON format.
        """
        commentaire = Commentaire.objects.get(pk=pk)
        if not Commentaire:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentaireSerializer(commentaire)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        """
        Handle DELETE requests to delete a specific comment by its ID.
        Returns a success message if the comment is deleted.
        """
        commentaire = Commentaire.objects.get(pk=pk)
        if not commentaire:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        commentaire.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk, *args, **kwargs):
        """
        Handle PUT requests to update a specific comment by its ID.
        Returns the updated comment in JSON format.
        """
        commentaire = Commentaire.objects.get(pk=pk)
        if not commentaire:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "titre": request.data.get("titre", commentaire.titre),
            "comment": request.data.get("comment", commentaire.comment),
        }

        serializer = CommentaireSerializer(commentaire, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)