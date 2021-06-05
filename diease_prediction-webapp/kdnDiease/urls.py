
from django.urls import path
from . import views

app_name = "kdnDiease"


urlpatterns = [
    path('predict_kdn/',views.predict_kdn),
    path('predict_kdn/predict/',views.kidney,name='submit_prediction_kdn'),
    path('predict_kdn/results_kdn/', views.view_kdn),

]