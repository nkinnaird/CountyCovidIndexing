import math
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV, PoissonRegressor
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
import sklearn.preprocessing as preprocessing 

import plotUtils as pu


def doSimpleLinearRegression(X, y, input_features):
    
    # first do cross validation to make sure the model is consistent
    
    kf = KFold(n_splits=5, shuffle=True, random_state = 715)
    cv_lm_r2s = [] #collect the validation results

    for train_ind, val_ind in kf.split(X,y):

        X_train, y_train = X[train_ind], y[train_ind]
        X_val, y_val = X[val_ind], y[val_ind] 

        #simple linear regression
        lm = LinearRegression()

        lm.fit(X_train, y_train)
        cv_lm_r2s.append(round(lm.score(X_val, y_val), 3))

    print('Simple regression scores: ', cv_lm_r2s, '\n')
    print(f'Simple mean cv r^2: {np.mean(cv_lm_r2s):.3f} +- {np.std(cv_lm_r2s):.3f}', '\n')
    
    # construct residuals plots from full fit in order to verify things look okay
    
    lm = LinearRegression()
    lm.fit(X,y)
    pred_y = lm.predict(X)
    residuals = pred_y - y
    
    print('Simple regression coef: ', lm.coef_, '\n')
    
    pu.makeMainResidualPlot(pred_y, residuals)
#     pu.makeFeatureResidualPlots(X, residuals, input_features)
    

def doPolynomialRegression(X, y, input_features):
    
    #poly with degree 2
    poly = preprocessing.PolynomialFeatures(degree=2, interaction_only=False)

    kf = KFold(n_splits=5, shuffle=True, random_state = 71)
    cv_lm_poly_r2s = []

    for train_ind, val_ind in kf.split(X,y):    

        X_train, y_train = X[train_ind], y[train_ind]
        X_val, y_val = X[val_ind], y[val_ind] 

        X_train_poly = poly.fit_transform(X_train)
        X_val_poly = poly.transform(X_val)

        lm_poly = LinearRegression()

        lm_poly.fit(X_train_poly, y_train)
        cv_lm_poly_r2s.append(round(lm_poly.score(X_val_poly, y_val), 3))

    print('Poly scores: ', cv_lm_poly_r2s, '\n')
    print(f'Poly mean cv r^2: {np.mean(cv_lm_poly_r2s):.3f} +- {np.std(cv_lm_poly_r2s):.3f}', '\n')
    
    
    X_poly = poly.fit_transform(X)
    lm_poly = LinearRegression()
    lm_poly.fit(X_poly,y)
    pred_y = lm_poly.predict(X_poly)
    residuals = pred_y - y
    
    print('Poly coef: ', lm_poly.coef_, '\n')
    
    pu.makeMainResidualPlot(pred_y, residuals)
#     pu.makeFeatureResidualPlots(X_poly, residuals, poly.get_feature_names(input_features))
    
    
    
def doLassoCV(X, y, poly=False):
    
    std = preprocessing.StandardScaler()
    
    # if true, then make polynomial features and then do LassoCV
    if(poly):
        poly = preprocessing.PolynomialFeatures(degree=2, interaction_only=False)
        X = poly.fit_transform(X)

    X_train_std = std.fit_transform(X)
    
#     alphavec = 10**np.linspace(-3,3,200)
#     lasso_model = LassoCV(alphas = alphavec, cv=5)
    
    lasso_model = LassoCV(cv=5, max_iter=10000, tol=1e-3)
    lasso_model.fit(X_train_std, y)
    
    r2score = round(lasso_model.score(X_train_std, y), 3)
    
    if(poly):
        print('LassoCV poly regression score: ', r2score, '\n')
        print('LassoCV poly alpha: ', lasso_model.alpha_, '\n')
        print('LassoCV poly coef: ', lasso_model.coef_, '\n')
    else:
        print('LassoCV simple regression score: ', r2score, '\n')
        print('LassoCV simple alpha: ', lasso_model.alpha_, '\n')
        print('LassoCV simple coef: ', lasso_model.coef_, '\n')
    
    
def doRidgeCV(X, y, poly=False):
    
    std = preprocessing.StandardScaler()
    
    # if true, then make polynomial features and then do RidgeCV
    if(poly):
        poly = preprocessing.PolynomialFeatures(degree=2, interaction_only=False)
        X = poly.fit_transform(X)

    X_train_std = std.fit_transform(X)
    
    alphavec = np.linspace(0,3,100)
    ridge_model = RidgeCV(alphas = alphavec, cv=5)
    
#     ridge_model = RidgeCV(cv=5)
    ridge_model.fit(X_train_std, y)
    
    r2score = round(ridge_model.score(X_train_std, y), 3)
    
    if(poly):
        print('RidgeCV poly regression score: ', r2score, '\n')
        print('RidgeCV poly alpha: ', ridge_model.alpha_, '\n')
        print('RidgeCV poly coef: ', ridge_model.coef_, '\n')
    else:
        print('RidgeCV simple regression score: ', r2score, '\n')
        print('RidgeCV simple alpha: ', ridge_model.alpha_, '\n')
        print('RidgeCV simple coef: ', ridge_model.coef_, '\n')    
    
    
    
    

# def doLassoRegression(X, y, inputAlpha):
    
#     kf = KFold(n_splits=5, shuffle=True, random_state = 42387)
#     r2s = [] #collect the validation results

#     for train_ind, val_ind in kf.split(X,y):

#         X_train, y_train = X[train_ind], y[train_ind]
#         X_val, y_val = X[val_ind], y[val_ind] 

#         # standard scale the features
#         std = preprocessing.StandardScaler()

#         X_train_std = std.fit_transform(X_train)
#         X_val_std = std.transform(X_val)

#         lasso_model = Lasso(alpha = inputAlpha)
#         lasso_model.fit(X_train_std,y_train)

#         r2s.append(round(lasso_model.score(X_val_std, y_val), 3))

#     print('Lasso regression scores: ', r2s, '\n')
#     print(f'Lasso mean cv r^2: {np.mean(r2s):.3f} +- {np.std(r2s):.3f}')
#     print(list(zip(X_train.columns, lasso_model.coef_)))