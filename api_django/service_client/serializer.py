from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Commentaire model.
    Converts model instances to JSON and vice versa.
    """

    class Meta:
        model = Client
        fields = ['id', 'genre', 'nom', 'prenom', 'email', 'telephone', 'mot_de_passe', 'date_creation']

