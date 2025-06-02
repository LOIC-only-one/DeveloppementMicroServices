from django.db import models

class Album(models.Model):
    titre = models.CharField(max_length=200)
    artiste = models.CharField(max_length=200)
    date_production = models.DateField()
    nombre_pistes = models.IntegerField()
    duree_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.titre} par {self.artiste}"
