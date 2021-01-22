import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats


def makeMainResidualPlot(prediction, y_residuals, saveplot=False):
    plt.figure(figsize=(10,5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(prediction, y_residuals)
    plt.title("Residuals vs Predicted")
    plt.xlabel("Predicted Deaths per 100k")
    plt.ylabel("Predicted - Actual Deaths per 100k")
    
    # Generates a probability plot of sample data against the quantiles of a 
    plt.subplot(1, 2, 2)
    stats.probplot(y_residuals, dist="norm", plot=plt)
    plt.title("Normal Q-Q plot")
    
    if(saveplot):
        plt.savefig("Images/FinalResidualsPlot.png")
    
def makeFeatureResidualPlots(X, y_residuals, input_features):
    
    for col in range(X.shape[1]):
        plt.figure()
        plt.scatter(X[:,col], y_residuals, alpha=0.2)
        plt.title("Residual feature plot")
        plt.xlabel(input_features[col])
        plt.ylabel("residuals")
    
def makeComparePlot(y, y_pred, saveplot=False):
    plt.figure(figsize=(7,7))
    
    plt.scatter(y_pred, y)
    plt.xlabel("Actual Deaths per 100k")
    plt.ylabel("Predicted Deaths per 100k")
    
    xpoints = ypoints = plt.xlim()
    plt.plot(xpoints, ypoints, linestyle='--', color='r', lw=3, scalex=False, scaley=False)
    
    plt.title('Predicted Target vs Actual Target')
    
    if(saveplot):
        plt.savefig("Images/FinalComparePlot.png")