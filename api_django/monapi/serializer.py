from rest_framework import serializers
from .models import Commentaire

class CommentaireSerializer(serializers.ModelSerializer):
    """
    Serializer for the Commentaire model.
    Converts model instances to JSON and vice versa.
    """

    class Meta:
        model = Commentaire
        fields = ['id', 'titre', 'comment', 'date']

