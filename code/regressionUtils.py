# methods for doing various regression fits with cross validation

import math
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV, PoissonRegressor
import sklearn.metrics as metrics
from sklearn.pipeline import Pipeline
import sklearn.preprocessing as preprocessing 


def printMetricResults(y_true, y_pred, boxcox_transformer):
    # Regression metrics
    r2=metrics.r2_score(y_true, y_pred)
    mean_absolute_error=metrics.mean_absolute_error(y_true, y_pred) 
    mse=metrics.mean_squared_error(y_true, y_pred) 

    print('r2: ', round(r2,4))
    print('MAE: ', round(mean_absolute_error,4), " - ", round(boxcox_transformer.inverse_transform(mean_absolute_error.reshape(1, -1))[0][0],1))
    print('MSE: ', round(mse,4), " - ", round(boxcox_transformer.inverse_transform(mse.reshape(1, -1))[0][0],1))
    print('RMSE: ', round(np.sqrt(mse),4), " - ", round(boxcox_transformer.inverse_transform(np.sqrt(mse).reshape(1, -1))[0][0],1))


def doSimpleLinearRegression(X, y):
    
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
    
    # fit model to all data and return it
    
    lm = LinearRegression()
    lm.fit(X,y)

    return lm
    

def doPolynomialRegression(X, y):
    
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
    
    # fit model to all data and return it along with feature transformers
    
    X_poly = poly.fit_transform(X)
    lm_poly = LinearRegression()
    lm_poly.fit(X_poly,y)
    
    return lm_poly, poly
    
    
def doLassoCV(X, y, poly=False):
    
    std = preprocessing.StandardScaler()
    
    # if true, then make polynomial features and then do LassoCV
    if(poly): 
        poly = preprocessing.PolynomialFeatures(degree=2, interaction_only=False)
        X = poly.fit_transform(X)
    
    X_train_std = std.fit_transform(X)
    
#     alphavec = 10**np.linspace(-4,2,100)
#     lasso_model = LassoCV(alphas = alphavec, cv=5, max_iter=5000, tol=1e-3)
    
    lasso_model = LassoCV(cv=5, max_iter=10000, tol=1e-3)
    lasso_model.fit(X_train_std, y)
    
    if(poly):
        return lasso_model, std, poly
    else:
        return lasso_model, std
    
    
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
    
    
    if(poly):
        return ridge_model, std, poly
    else:
        return ridge_model, std
    