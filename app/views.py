from django.shortcuts import render
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import json

import warnings

warnings.filterwarnings('ignore')

# Create your views here.
def index(request):
    return render(request, 'index.html')


def results(request):
    selected = request.POST.getlist('x-encoding')
    # print(type(selected))

    df = pd.read_csv('C:/Users/Minee/Desktop/css_workspace/django-proj/pj/app/diabetes.csv')
    
    corr_df = df.corr()
    corr_df = corr_df.apply(lambda x: round(x ,1))
    fig, ax = plt.subplots()
    im = ax.imshow(corr_df,cmap='Greys')
    cbar = ax.figure.colorbar(im, ax=ax)

    ax.set_xticks(np.arange(len(corr_df.columns)))
    ax.set_yticks(np.arange(len(corr_df.index)))

    ax.set_xticklabels(corr_df.columns)
    ax.set_yticklabels(corr_df.columns)

    for x in range(len(corr_df.columns)):
        for y in range(len(corr_df.index)):
            ax.text(y, x, corr_df.iloc[y, x], ha='center', va='center', color='g')
    plt.xticks(rotation=90)
    fig.tight_layout()     
    plt.savefig('./static/images/heatmap.png')
    # print("1")

    df = pd.read_csv('C:/Users/Minee/Desktop/css_workspace/django-proj/pj/app/diabetes.csv')
    correl_out = []
    correl_dep = [[]]
    dep_var = ['Pregnancies', 'Glucose','BloodPressure','SkinThickness','Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    indep_var = 'Outcome'
    for item in dep_var:
        # print(item)
        x = df[item].values
        y = df[indep_var].values
        correl_out.append(stats.pearsonr(x,y)[0])
    # data_corr: Correlation Coefficient between dependent variables and independent variable
    data_corr = np.concatenate((dep_var,correl_out),axis=0).reshape(2,8)
    data_corr = { dep_var[i] : correl_out[i]  for i in range(len(dep_var))}
    selected_corr_out = []
    for var in selected:
        x = df[var].values
        y = df[indep_var].values
        selected_corr_out.append(stats.pearsonr(x,y)[0])
    data_selected = { selected[i] : selected_corr_out[i]  for i in range(len(selected))}
    sorted_data_selected = sorted(data_selected.items(), key = lambda item: item[1])
    x = (sorted_data_selected[-2], sorted_data_selected[-1])
    new_data = dict((x,y) for x,y in x)
    # print(new_data)
    # print('????',data_corr, correl_out)

    context = {
        'data': data_corr,
        'new_data':new_data
    }
    return render(request,  'results.html', context)




# for item in ['Pregnancies', 'Glucose','BloodPressure','SkinThickness','Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']:
#     print(item) 
#     x = df[item].values
#     print('Covariance: {:.2f}'.format(np.cov(x,y)[0,1]))
#     print('Correlation: {:.2f}'.format(stats.pearsonr(x,y)[0]))
#     print('P-Value: {:.4f}'.format(stats.pearsonr(x,y)[1]))
#     print("\n")
# x= df.Pregnancies.values.reshape(-1,1)
# y = df.Outcome.values.reshape(-1,1)
# import statsmodels.api as sm
# for item in ['Pregnancies', 'Glucose','BloodPressure','SkinThickness','Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']:
#     x = df[item].values
#     results = sm.OLS(y,sm.add_constant(x)).fit()
#     print(results.summary())