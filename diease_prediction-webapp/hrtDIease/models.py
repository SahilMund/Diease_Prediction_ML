from django.db import models

# Create your models here.

class HeartPredResults(models.Model):

    Age = models.FloatField()
    Sex = models.FloatField()
    chest_pain = models.FloatField()
    trestbps = models.FloatField()
    chol = models.FloatField()
    fbs = models.FloatField()
    restecg = models.FloatField()
    thalach = models.FloatField()
    exang = models.FloatField()
    oldpeak = models.FloatField()
    slope = models.FloatField()
    ca = models.FloatField()
    thal = models.FloatField()

    PredictRes = models.CharField(max_length=30)
    Accuracy = models.FloatField()

   

    def __str__(self):
        return self.PredictRes