from django.shortcuts import render
from django.shortcuts import render
import pandas as pd
import numpy as np
from django.http import JsonResponse
from .models import HeartPredResults
# Create your views here.

def predict_hrt(request):
    return render(request,"heart.html")


# ------------------------------------heart diease------------------------
def heart(request):
    df=pd.read_csv(r"C:\Users\msahi\OneDrive\Desktop\c\majorpro_app\dataset\heart.csv")
    
    #Remove Duplicates
    df.drop_duplicates(inplace = True)

    #outlier remove process...
    #IQR inter quartile range

    Q1=df.quantile(0.25)
    Q3=df.quantile(0.75)
    IQR=Q3-Q1
    data_out = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]

    #extract feature and target
    X=data_out.drop(columns=['target'])
    y=data_out['target']

    #split the dataset into train and test 10%
    from sklearn.model_selection import train_test_split

    X_train,X_test,Y_train,Y_test=train_test_split(X,y,test_size=0.25,random_state=5)

    #Using GaussianNB 
    from sklearn.naive_bayes import GaussianNB
    gauss = GaussianNB()
    gauss.fit(X_train, Y_train)

    Y_pred = gauss.predict(X_test)
    from sklearn.metrics import accuracy_score
    acc = round(accuracy_score(Y_test,Y_pred),2)*100


    # accepting values from fronted
    
    Age=float(request.POST.get('Age'))
    Sex =  float(request.POST.get('Sex'))
    chest_pain = float(request.POST.get('chest_pain'))
    trestbps =  float(request.POST.get('trestbps'))
    chol =   float(request.POST.get('chol'))
    fbs =   float(request.POST.get('fbs'))
    restecg=   float(request.POST.get('restecg'))
    thalach  =  float(request.POST.get('thalach'))
    exang  =  float(request.POST.get('exang'))
    oldpeak  =  float(request.POST.get('oldpeak'))
    slope  =  float(request.POST.get('slope'))
    ca  =  float(request.POST.get('ca'))
    thal  =  float(request.POST.get('thal'))

    vals=[
       Age,Sex,chest_pain,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,
       slope,ca,thal
    ]

    pred = gauss.predict([vals])

    PredictRes=""
    if pred == [1]:
        PredictRes = "Positive"
    else:
        PredictRes = "Negative"

    
    HeartPredResults.objects.create(Age=Age, Sex=Sex,
     chest_pain=chest_pain,trestbps=trestbps, chol=chol,fbs=fbs,restecg=restecg,thalach=thalach,
     exang=exang,oldpeak=oldpeak,slope=slope,ca=ca,thal=thal,
     PredictRes=PredictRes,Accuracy=acc)

    return JsonResponse({'result': PredictRes,'accuracy':acc,
    'Age':Age, 'Sex':Sex,
     'chest_pain':chest_pain,'trestbps':trestbps, 'chol':chol,'fbs':fbs,
     'restecg':restecg,
     'thalach':thalach,'exang':exang,'oldpeak':oldpeak,'slope':slope,
     'ca':ca,'thal':thal },safe=False)



def view_hrt(request):
    # Submit prediction and show all
    data = {"dataset": HeartPredResults.objects.all().order_by("-id")}
    return render(request, "dbview/dbheart.html", data)



