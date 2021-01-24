# Predicting US County Covid-19 Deaths with US Census Data

### Objective:
---

Predict US county Covid-19 deaths scaled by population using US census data in order to identify those counties which are more at risk than others. By identifying these counties, resources can be deployed more efficiently. 

### Methodology:
---

US county-level census and Covid-19 data were scraped from the US Census Bureau and downloaded from the New York Times GitHub repository respectively. The target variable selected was cumulative Covid-19 deaths scaled by population. (Originally Covid-19 data was scraped via Selenium from the CDC, however the predictive model was ineffective.) The target variable was scaled by population in order to avoid identifying those counties which simply had the most people. A simple linear regression model was tested along with LASSO and Ridge regressions, all of which were tested with and without polynomial features. Ultimately the best performing model, LASSO with polynomial features, was chosen as the final model due to it's best performance. All models were tested with cross-validation routines in order to verify model stability. 



A presentation on the project can be found [here](Presentation/CovidProjectPresentation.pdf).


### Results:
---





### Data:
---

- US county-level census data scraped from the Census Bureau [QuickFacts](https://www.census.gov/quickfacts/fact/table/) page
- Covid-19 county-level data dated 01/18/2021 from the New York Times GitHub [repository](https://github.com/nytimes/covid-19-data)
- Covid-19 county-level data scraped from the CDC [data tracker](https://covid.cdc.gov/covid-data-tracker/#county-view) (this was ultimately not used in the project)


### Tools used:
---

- BeautifulSoup and Selenium for web scraping (the Selenium-acquired data was ultimately not used)
- Feature engineering, Box-Cox transform and polynomial features
- Linear regression
- Regularization via LASSO and Ridge regression
- Cross validation
- Matplotlib, Seaborn, Plotly for visualization


### Code details:
---


`this is code right`











