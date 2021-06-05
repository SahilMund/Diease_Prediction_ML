from django.db import models


# Create your models here.

class KdnPredResults(models.Model):

    age = models.FloatField()
    blood_pressure = models.FloatField()
    specific_gravity = models.FloatField()
    albumin = models.FloatField()
    sugar = models.FloatField()
    red_blood_cells = models.FloatField()
    pus_cell = models.FloatField()
    pus_cell_clumps = models.FloatField()
    bacteria = models.FloatField()
    blood_glucose_random = models.FloatField()

    blood_urea = models.FloatField()
    serum_creatinine = models.FloatField()
    sodium = models.FloatField()
    hemoglobin = models.FloatField()
    packed_cell_volume = models.FloatField()
    white_blood_cell_count = models.FloatField()
    red_blood_cell_count = models.FloatField()
    hypertension = models.FloatField()
    diabetes_mellitus = models.FloatField()
    coronary_artery_disease = models.FloatField()

    appetite = models.FloatField()
    pedal_edema = models.FloatField()
    anemia = models.FloatField()
    

    PredictRes = models.CharField(max_length=30)
    Accuracy = models.FloatField()

   

    def __str__(self):
        return self.PredictRes