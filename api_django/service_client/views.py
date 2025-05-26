from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializer import ClientSerializer
from rest_framework import permissions


class ClientViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve all comments.
        Returns a list of comments in JSON format.
        """
        commentaires = Client.objects.all()
        id = request.query_params.get('id', None)
        serializer = ClientSerializer(commentaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            "genre": request.data.get("genre"),
            "nom": request.data.get("nom"),
            "prenom": request.data.get("prenom"),
            "email": request.data.get("email"),
            "telephone": request.data.get("telephone"),
            "mot_de_passe": request.data.get("mot_de_passe"),
        }

        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ClientViewAPIDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Handle GET requests to retrieve a specific comment by its ID.
        Returns the comment in JSON format.
        """
        commentaire = Client.objects.get(pk=pk)
        if not Client:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientSerializer(commentaire)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        """
        Handle DELETE requests to delete a specific comment by its ID.
        Returns a success message if the comment is deleted.
        """
        commentaire = Client.objects.get(pk=pk)
        if not commentaire:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        commentaire.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk, *args, **kwargs):
        """
        Handle PUT requests to update a specific comment by its ID.
        Returns the updated comment in JSON format.
        """
        commentaire = Client.objects.get(pk=pk)
        if not commentaire:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "genre": request.data.get("genre", commentaire.genre),
            "nom": request.data.get("nom", commentaire.nom),
            "prenom": request.data.get("prenom", commentaire.prenom),
            "email": request.data.get("email", commentaire.email),
            "telephone": request.data.get("telephone", commentaire.telephone),
            "mot_de_passe": request.data.get("mot_de_passe", commentaire.mot_de_passe),
        }

        serializer = ClientSerializer(commentaire, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientViewAPIFilter(APIView):
    """
    API view to filter clients based on genre.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user, *args, **kwargs):
        """
        On récupère tout les clients créer par l'utilisateur connecté.
        """
        clients = Client.objects.filter(user=user)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
