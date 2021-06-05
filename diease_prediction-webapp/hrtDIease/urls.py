
from django.urls import path
from . import views

app_name = "hrtDIease"


urlpatterns = [
    path('predict_hrt/',views.predict_hrt),
    path('predict_hrt/predict/',views.heart,name='submit_prediction_heart'),
    path('predict_hrt/results_hrt/', views.view_hrt)

]