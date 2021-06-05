from django.urls import path
from . import views

app_name = "diabDiease"


urlpatterns = [
    path('',views.home),
    path('predict_diab/',views.predict_diab),
    path('predict_diab/predict/',views.diabetes,name='submit_prediction'),
    path('predict_diab/results_diab/', views.view_diab),

]