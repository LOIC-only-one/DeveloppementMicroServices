from django.db import models

# Create your models here.

class Commentaire(models.Model):
    """
    Model representing a comment.
    """
    titre = models.CharField(max_length=100, verbose_name="Titre")
    comment = models.TextField(verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        """
        String representation of the Commentaire model.
        Returns the title of the comment.
        """
        return self.titre
    
    def __repr__(self):
        return super().__repr__()
