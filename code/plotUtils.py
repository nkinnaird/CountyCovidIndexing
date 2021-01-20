import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats


def makeMainResidualPlot(prediction, y_residuals):
    plt.figure(figsize=(10,5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(prediction, y_residuals)
    plt.title("Residual plot")
    plt.xlabel("prediction")
    plt.ylabel("residuals")
    
    # Generates a probability plot of sample data against the quantiles of a 
    plt.subplot(1, 2, 2)
    stats.probplot(y_residuals, dist="norm", plot=plt)
    plt.title("Normal Q-Q plot")
    
def makeFeatureResidualPlots(X, y_residuals):
#     plt.figure()
    
    for col in range(X.shape[1]):
        plt.figure()
        plt.scatter(X[:,col], y_residuals)
        plt.title("Residual feature plot")
        plt.xlabel(f'feature {col}')
        plt.ylabel("residuals")
    
