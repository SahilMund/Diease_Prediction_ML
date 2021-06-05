from django.db import models

# Create your models here.

class DiabPredResults(models.Model):

    Pregnencies = models.FloatField()
    Glucose = models.FloatField()
    Blood_Pressure = models.FloatField()
    Skin_Thickness = models.FloatField()
    Insulin = models.FloatField()
    BMI = models.FloatField()
    DPF = models.FloatField()
    Age = models.FloatField()
    PredictRes = models.CharField(max_length=30)
    Accuracy = models.FloatField()

   

    def __str__(self):
        return self.PredictRes
