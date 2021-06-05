
from django.urls import path
from . import views

app_name = "brstDiease"


urlpatterns = [
    path('predict_breast/',views.predict_breast),
    path('predict_breast/predict/',views.breastCancer,name='submit_prediction_brst'),
    path('predict_breast/results_breast/', views.view_brst),


]