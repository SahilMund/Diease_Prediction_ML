from django.shortcuts import render
import pandas as pd
import numpy as np
from django.http import JsonResponse
from .models import DiabPredResults

# Create your views here.

def home(request):
    return render(request,"home.html")

def predict_diab(request):
    return render(request,"diabetes.html")

# -------------------------------------- diabetes-------------------------
def diabetes(request):
    
    df=pd.read_csv(r"C:\Users\msahi\OneDrive\Desktop\c\majorpro_app\dataset\diabetes.csv")

    # It is better to replace zeros with nan since after that counting them would be easier and zeros need to be replaced with suitable values¶

    df_c = df.copy()
    df_c[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = df_c[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)

    #Taking care of missing values  using imputer class
    from sklearn.base import TransformerMixin

    class DataFrameImputer(TransformerMixin):
        
        def fit(self, X, y=None):

            self.fill = pd.Series([X[c].value_counts().index[0]
                if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
                index=X.columns)

            return self

        def transform(self, X, y=None):
            return X.fillna(self.fill)
    df_c = pd.DataFrame(df)
    df_c = DataFrameImputer().fit_transform(df_c)


    #outlier remove process...
    #IQR inter quartile range
    df=df_c.copy()
    Q1=df.quantile(0.15)
    Q3=df.quantile(0.85)
    IQR=Q3-Q1
    data_out = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]

    df=data_out.copy()

    # Splitting into dependant and independant variables

    X=df.drop('Outcome',axis=1)
    Y=df['Outcome']

    #split the dataset into train and test 
    from sklearn.model_selection import train_test_split

    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.25,random_state=5)

   

    #Using SVC linear
    from sklearn.svm import SVC
    svc_lin = SVC(kernel = 'linear', random_state = 0)
    svc_lin.fit(X_train, Y_train)

    Y_pred = svc_lin.predict(X_test)
    from sklearn.metrics import accuracy_score
    acc = round(accuracy_score(Y_test,Y_pred),2)*100

    # accepting values from fronted
    
    Pregnencies=float(request.POST.get('Pregnencies'))
    Glucose =  float(request.POST.get('Glucose'))
    Blood_Pressure = float(request.POST.get('Blood_Pressure'))
    Skin_Thickness =  float(request.POST.get('Skin_Thickness'))
    Insulin =   float(request.POST.get('Insulin'))
    BMI =   float(request.POST.get('BMI'))
    DPF=   float(request.POST.get('DPF'))
    Age  =  float(request.POST.get('Age'))

    vals=[Pregnencies,Glucose,Blood_Pressure,Skin_Thickness,Insulin,BMI,DPF,Age]



    pred = svc_lin.predict([vals])


    PredictRes=""
    if pred == [1]:
        PredictRes = "Positive"
    else:
        PredictRes = "Negative"

    DiabPredResults.objects.create(Pregnencies=Pregnencies, Glucose=Glucose, Blood_Pressure=Blood_Pressure,

     Skin_Thickness=Skin_Thickness, Insulin=Insulin,BMI=BMI,DPF=DPF,Age=Age,PredictRes=PredictRes,Accuracy=acc)

    return JsonResponse({'result': PredictRes,'accuracy':acc,'Pregnencies': Pregnencies,
                'Glucose':Glucose,'Blood_Pressure':Blood_Pressure, 'Skin_Thickness':Skin_Thickness,
                     'Insulin':Insulin,'BMI':BMI,'DPF':DPF,'Age':Age},safe=False)




# -------------------------databases------------------------------------

def view_diab(request):
    # Submit prediction and show all
    data = {"dataset": DiabPredResults.objects.all().order_by("-id")}
    return render(request, "dbview/dbdiab.html", data)


