from django.db import models

# Create your models here.

class Client(models.Model):
    """
    Model representing a client.
    """

    id = models.AutoField(primary_key=True, verbose_name="ID")
    
    genre = models.CharField(
        max_length=10,
        choices=[
            ('M', 'Monsieur'),
            ('Mme', 'Madame'),
            ('Mlle', 'Mademoiselle')
        ],
        verbose_name="Genre"
    )

    nom = models.CharField(max_length=50, verbose_name="Nom")
    prenom = models.CharField(max_length=50, verbose_name="Prénom")
    email = models.EmailField(max_length=254, verbose_name="Email")
    telephone = models.CharField(max_length=15, verbose_name="Téléphone", blank=True, null=True)
    mot_de_passe = models.CharField(
        max_length=128,
        verbose_name="Mot de passe",
        help_text="Le mot de passe doit contenir au moins 8 caractères."
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )


    def __str__(self):
        """
        String representation of the Client model.
        Returns the full name of the client.
        """
        return f"{self.prenom} {self.nom}"
    
    def __repr__(self):
        return super().__repr__()