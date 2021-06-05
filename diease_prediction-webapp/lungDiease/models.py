from django.db import models

# Create your models here.

class LungPredResults(models.Model):

    Age = models.FloatField()
    Smokes = models.FloatField()
    AreaQ = models.FloatField()
    Alkohol = models.FloatField()
    
    PredictRes = models.CharField(max_length=30)
    Accuracy = models.FloatField()

   

    def __str__(self):
        return self.PredictRes
