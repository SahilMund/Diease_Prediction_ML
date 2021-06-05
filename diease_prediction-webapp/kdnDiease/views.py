from django.shortcuts import render
import pandas as pd
import numpy as np
from django.http import JsonResponse
from .models import KdnPredResults

# Create your views here.


def predict_kdn(request):
    return render(request, "kidney.html")


def kidney(request):
    df = pd.read_csv(
        r"C:\Users\msahi\OneDrive\Desktop\c\majorpro_app\dataset\kidney_disease.csv")

    # Renaming the column names
    col_dict = {"bp": "blood_pressure",
                "sg": "specific_gravity",
                "al": "albumin",
                "su": "sugar",
                "rbc": "red_blood_cells",
                "pc": "pus_cell",
                "pcc": "pus_cell_clumps",
                "ba": "bacteria",
                "bgr": "blood_glucose_random",
                "bu": "blood_urea",
                "sc": "serum_creatinine",
                "sod": "sodium",
                "pot": "potassium",
                "hemo": "hemoglobin",
                "pcv": "packed_cell_volume",
                "wc": "white_blood_cell_count",
                "rc": "red_blood_cell_count",
                "htn": "hypertension",
                "dm": "diabetes_mellitus",
                "cad": "coronary_artery_disease",
                "appet": "appetite",
                "pe": "pedal_edema",
                "ane": "anemia"}
    df.rename(columns=col_dict, inplace=True)

    df = df.drop(['id'], axis=1)

    # dividing & storing numerical and alphabetical datas
    numerical = []
    categorical = []  # alphabetical data
    for i in df.columns:
        if (df[i].dtypes) == 'O':  # object
            categorical.append(i)
        else:
            numerical.append(i)

    df.replace(to_replace={'\t43': '43', '\t6200': '6200', '\t8400': '8400',
               '\t?': np.nan, 'ckd\t': 1, 'ckd': 1, 'notckd': 0}, inplace=True)

    map_values = {'normal': 0, 'abnormal': 1, 'notpresent': 0, 'present': 1,
                  'yes': 1, 'no': 0, '\tno': 0, '\tyes': 1, ' yes': 1, 'good': 1, 'poor': 0}
    df.replace(to_replace=map_values, inplace=True)

    # Taking care of missing values  using imputer class

    from sklearn.base import TransformerMixin

    class DataFrameImputer(TransformerMixin):

        def fit(self, X, y=None):

            self.fill = pd.Series([X[c].value_counts().index[0]
                                   if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
                                  index=X.columns)

            return self

        def transform(self, X, y=None):
            return X.fillna(self.fill)
    df = pd.DataFrame(df)
    df = DataFrameImputer().fit_transform(df)

    # corelation output is very less so dropping one table
    df = df.drop(['potassium'], axis=1)

    X = df.drop('classification', axis=1)
    Y = df['classification']

    # split the dataset into train and test
    from sklearn.model_selection import train_test_split

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.25, random_state=5)

    # Using Logistic Regression
    from sklearn.linear_model import LogisticRegression
    log = LogisticRegression(random_state=0)
    log.fit(X_train, Y_train)

    Y_pred = log.predict(X_test)
    from sklearn.metrics import accuracy_score
    acc = round(accuracy_score(Y_test, Y_pred), 2)*100

    # accepting values from fronted

    age = float(request.POST.get('age'))
    blood_pressure = float(request.POST.get('blood_pressure'))
    specific_gravity = float(request.POST.get('specific_gravity'))
    albumin = float(request.POST.get('albumin'))
    sugar = float(request.POST.get('sugar'))
    red_blood_cells = float(request.POST.get('red_blood_cells'))
    pus_cell = float(request.POST.get('pus_cell'))
    pus_cell_clumps = float(request.POST.get('pus_cell_clumps'))
    bacteria = float(request.POST.get('bacteria'))
    blood_glucose_random = float(request.POST.get('blood_glucose_random'))
    blood_urea = float(request.POST.get('blood_urea'))
    serum_creatinine = float(request.POST.get('serum_creatinine'))
    sodium = float(request.POST.get('sodium'))
    hemoglobin = float(request.POST.get('hemoglobin'))
    packed_cell_volume = float(request.POST.get('packed_cell_volume'))
    white_blood_cell_count = float(request.POST.get('white_blood_cell_count'))
    red_blood_cell_count = float(request.POST.get('red_blood_cell_count'))
    hypertension = float(request.POST.get('hypertension'))
    diabetes_mellitus = float(request.POST.get('diabetes_mellitus'))
    coronary_artery_disease = float(request.POST.get('coronary_artery_disease'))
    appetite = float(request.POST.get('appetite'))
    pedal_edema = float(request.POST.get('pedal_edema'))
    anemia = float(request.POST.get('anemia'))

    vals = [age, blood_pressure, specific_gravity, albumin, 
    sugar, red_blood_cells, pus_cell, pus_cell_clumps, 
    bacteria, blood_glucose_random,blood_urea, serum_creatinine,
     sodium, hemoglobin, packed_cell_volume,white_blood_cell_count, 
     red_blood_cell_count, hypertension, diabetes_mellitus,coronary_artery_disease,
      appetite, pedal_edema, anemia]

    pred = log.predict([vals])

    PredictRes = ""
    if pred == [1]:
        PredictRes = "Positive"
    else:
        PredictRes = "Negative"

    KdnPredResults.objects.create(age=age, blood_pressure=blood_pressure,
                                   specific_gravity=specific_gravity, albumin=albumin,
                                    sugar=sugar,
                                   red_blood_cells=red_blood_cells, 
                                   pus_cell=pus_cell,
                                   pus_cell_clumps=pus_cell_clumps,
                                   bacteria=bacteria,
                                   blood_glucose_random=blood_glucose_random,

                                   blood_urea=blood_urea,
                                   serum_creatinine=serum_creatinine,
                                   sodium=sodium,
                                   hemoglobin=hemoglobin,
                                   packed_cell_volume=packed_cell_volume,
                                   white_blood_cell_count=white_blood_cell_count,
                                   red_blood_cell_count=red_blood_cell_count,
                                   hypertension=hypertension,
                                   diabetes_mellitus=diabetes_mellitus,
                                   coronary_artery_disease=coronary_artery_disease,

                                   appetite=appetite,
                                   pedal_edema=pedal_edema,
                                   anemia=anemia,
                                  

                                   PredictRes=PredictRes, Accuracy=acc)

    return JsonResponse({'result': PredictRes, 'accuracy': acc,
                         'age': age, 
                         'blood_pressure': blood_pressure, 
                         'specific_gravity': specific_gravity,
                         'albumin': albumin, 
                         'sugar': sugar,
                          'red_blood_cells': red_blood_cells, 
                          'pus_cell': pus_cell,
                         'pus_cell_clumps': pus_cell_clumps,
                         'bacteria': bacteria,
                         'blood_glucose_random': blood_glucose_random,

                         'blood_urea': blood_urea,
                         'serum_creatinine': serum_creatinine,
                         'sodium': sodium,
                         'hemoglobin': hemoglobin,
                         'packed_cell_volume': packed_cell_volume,
                         'white_blood_cell_count': white_blood_cell_count,
                         'red_blood_cell_count': red_blood_cell_count,
                         'hypertension': hypertension,
                         'diabetes_mellitus': diabetes_mellitus,
                         'coronary_artery_disease': coronary_artery_disease,

                         'appetite': appetite,
                         'pedal_edema': pedal_edema,
                         'anemia': anemia

                         }, safe=False)


def view_kdn(request):
    # Submit prediction and show all
    data = {"dataset": KdnPredResults.objects.all().order_by("-id")}
    return render(request, "dbview/dbkdn.html", data)
