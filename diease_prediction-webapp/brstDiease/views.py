from django.shortcuts import render
import pandas as pd
import numpy as np
from django.http import JsonResponse

from .models import BrstPredResults


def predict_breast(request):
    return render(request, "breast_cancer.html")


def breastCancer(request):
    df = pd.read_csv(
        r"C:\Users\msahi\OneDrive\Desktop\c\majorpro_app\dataset\breast-data.csv")
    df = df.drop(['Unnamed: 32', 'id'], axis=1)

    # converting to 0 and 1
    a = {'M': 1, 'B': 0}
    df['diagnosis'] = df['diagnosis'].replace(a)

    # slicing of  df dataset  to get independent(X/source) and dependent(y/target) variables
    X = df.drop(['diagnosis'], axis=1)
    y = df.diagnosis

    # Splitting the datasets into 75% traning and 25% testing
    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, y, test_size=0.25, random_state=0)

    # Using RandomForestClassifier method of ensemble class to use Random Forest Classification algorithm
    from sklearn.ensemble import RandomForestClassifier
    forest = RandomForestClassifier(
        n_estimators=10, criterion='entropy', random_state=0)
    forest.fit(X_train, Y_train)
    Y_pred = forest.predict(X_test)
    from sklearn.metrics import accuracy_score
    acc = round(accuracy_score(Y_test, Y_pred), 2)*100

    # accepting values from fronted
    radius_mean = float(request.POST.get('radius_mean'))
    texture_mean = float(request.POST.get('texture_mean'))
    perimeter_mean = float(request.POST.get('perimeter_mean'))
    area_mean = float(request.POST.get('area_mean'))
    smoothness_mean = float(request.POST.get('smoothness_mean'))
    compactness_mean = float(request.POST.get('compactness_mean'))
    concavity_mean = float(request.POST.get('concavity_mean'))
    concave_points_mean = float(request.POST.get('concave_points_mean'))
    symmetry_mean = float(request.POST.get('symmetry_mean'))
    fractal_dimension_mean = float(request.POST.get('fractal_dimension_mean'))
    radius_se = float(request.POST.get('radius_se'))
    texture_se = float(request.POST.get('texture_se'))
    perimeter_se = float(request.POST.get('perimeter_se'))
    area_se = float(request.POST.get('area_se'))
    smoothness_se = float(request.POST.get('smoothness_se'))
    compactness_se = float(request.POST.get('compactness_se'))
    concavity_se = float(request.POST.get('concavity_se'))
    concave_points_se = float(request.POST.get('concave_points_se'))
    symmetry_se = float(request.POST.get('symmetry_se'))
    fractal_dimension_se = float(request.POST.get('fractal_dimension_se'))
    radius_worst = float(request.POST.get('radius_worst'))
    texture_worst = float(request.POST.get('texture_worst'))
    perimeter_worst = float(request.POST.get('perimeter_worst'))
    area_worst = float(request.POST.get('area_worst'))
    smoothness_worst = float(request.POST.get('smoothness_worst'))
    compactness_worst = float(request.POST.get('compactness_worst'))
    concavity_worst = float(request.POST.get('concavity_worst'))
    concave_points_worst = float(request.POST.get('concave_points_worst'))
    symmetry_worst = float(request.POST.get('symmetry_worst'))
    fractal_dimension_worst = float(request.POST.get('fractal_dimension_worst'))

    vals = [radius_mean, texture_mean, perimeter_mean,
            area_mean, smoothness_mean, compactness_mean,
            concavity_mean, concave_points_mean, symmetry_mean,
            fractal_dimension_mean,
            radius_se, texture_se, perimeter_se, area_se,
            smoothness_se,
            compactness_se, concavity_se, concave_points_se,
            symmetry_se,
            fractal_dimension_se,
            radius_worst,
            texture_worst, perimeter_worst, area_worst,
            smoothness_worst,
            compactness_worst, concavity_worst, concave_points_worst, symmetry_worst,
            fractal_dimension_worst]

    pred = forest.predict([vals])

    PredictRes = ""
    if pred == [1]:
        PredictRes = "Positive"
    else:
        PredictRes = "Negative"

    BrstPredResults.objects.create(radius_mean=radius_mean, texture_mean=texture_mean,
                                   perimeter_mean=perimeter_mean, area_mean=area_mean, smoothness_mean=smoothness_mean,
                                   compactness_mean=compactness_mean, concavity_mean=concavity_mean,
                                   concave_points_mean=concave_points_mean,
                                   symmetry_mean=symmetry_mean,
                                   fractal_dimension_mean=fractal_dimension_mean,
                                   radius_se=radius_se,
                                   texture_se=texture_se,
                                   perimeter_se=perimeter_se,
                                   area_se=area_se,
                                   smoothness_se=smoothness_se,
                                   compactness_se=compactness_se,
                                   concavity_se=concavity_se,
                                   concave_points_se=concave_points_se,
                                   symmetry_se=symmetry_se,
                                   fractal_dimension_se=fractal_dimension_se,
                                   radius_worst=radius_worst,
                                   texture_worst=texture_worst,
                                   perimeter_worst=perimeter_worst,
                                   area_worst=area_worst,
                                   smoothness_worst=smoothness_worst,
                                   compactness_worst=compactness_worst,
                                   concavity_worst=concavity_worst,
                                   concave_points_worst=concave_points_worst,
                                   symmetry_worst=symmetry_worst,
                                   fractal_dimension_worst=fractal_dimension_worst,

                                   PredictRes=PredictRes, Accuracy=acc)

    return JsonResponse({'result': PredictRes, 'accuracy': acc,
                         'radius_mean': radius_mean, 'texture_mean': texture_mean, 
                         'perimeter_mean': perimeter_mean,
                         'area_mean': area_mean, 'smoothness_mean': smoothness_mean,
                          'compactness_mean': compactness_mean, 'concavity_mean': concavity_mean,
                         'concave_points_mean': concave_points_mean,
                         'symmetry_mean': symmetry_mean,
                         'fractal_dimension_mean': fractal_dimension_mean,
                         'radius_se': radius_se,
                         'texture_se': texture_se,
                         'perimeter_se': perimeter_se,
                         'area_se': area_se,
                         'smoothness_se': smoothness_se,
                         'compactness_se': compactness_se,
                         'concavity_se': concavity_se,
                         'concave_points_se': concave_points_se,
                         'symmetry_se': symmetry_se,
                         'fractal_dimension_se': fractal_dimension_se,
                         'radius_worst': radius_worst,
                         'texture_worst': texture_worst,
                         'perimeter_worst': perimeter_worst,
                         'area_worst': area_worst,
                         'smoothness_worst': smoothness_worst,
                         'compactness_worst': compactness_worst,
                         'concavity_worst': concavity_worst,
                         'concave_points_worst': concave_points_worst,
                         'symmetry_worst': symmetry_worst,
                         'fractal_dimension_worst': fractal_dimension_worst


                         }, safe=False)


def view_brst(request):
    # Submit prediction and show all
    data = {"dataset": BrstPredResults.objects.all().order_by("-id")}
    return render(request, "dbview/dbbrst.html", data)
