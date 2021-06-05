

from django.urls import path
from . import views

app_name = "lungDiease"


urlpatterns = [
    path('predict_lung/',views.predict_lung),
    path('predict_lung/predict/',views.lung,name='submit_prediction_lung'),
    path('predict_lung/results_lung/', views.view_lung)

]