from django.shortcuts import render
import pandas as pd
import numpy as np
from django.http import JsonResponse

from . models import LungPredResults

# Create your views here.


def predict_lung(request):
    return render(request, "lung.html")


# ----------------------------------lung cancer----------------------

def lung(request):
    df = pd.read_csv(
        r"C:\Users\msahi\OneDrive\Desktop\c\majorpro_app\dataset\lung_cancer.csv")
    # drop the unnecessary features like name surname
    df = df.drop(['Name', 'Surname'], axis=1)

    X = df.drop('Result', axis=1)
    Y = df['Result']

    # split the dataset into train and test
    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.25, random_state=5)

    # Using Logistic Regression
    from sklearn.linear_model import LogisticRegression
    log_reg = LogisticRegression(random_state=0)
    log_reg.fit(X_train, Y_train)

    Y_pred = log_reg.predict(X_test)
    from sklearn.metrics import accuracy_score
    acc = round(accuracy_score(Y_test, Y_pred), 2)*100

    # accepting values from fronted

    Age = float(request.POST.get('age'))
    Smokes = float(request.POST.get('smokes'))
    AreaQ = float(request.POST.get('areaq'))
    Alkohol = float(request.POST.get('alkohol'))

    vals = [Age,Smokes,AreaQ,Alkohol]

    pred = log_reg.predict([vals])

    PredictRes = ""
    if pred == [1]:
        PredictRes = "Positive"
    else:
        PredictRes = "Negative"


        
    LungPredResults.objects.create(Age=Age, Smokes=Smokes, AreaQ=AreaQ,

     Alkohol=Alkohol,PredictRes=PredictRes,Accuracy=acc)

    return JsonResponse({'result': PredictRes,'accuracy':acc,'Age': Age,
                'Smokes':Smokes,'AreaQ':AreaQ, 'Alkohol':Alkohol},safe=False)



# -------------------------databases------------------------------------

def view_lung(request):
    # Submit prediction and show all
    data = {"dataset": LungPredResults.objects.all().order_by("-id")}
    return render(request, "dbview/dblung.html", data)



    