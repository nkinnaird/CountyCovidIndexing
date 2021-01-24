# Predicting US County Covid-19 Deaths with US Census Data

### Objective:

Predict US county Covid-19 deaths scaled by population using US census data in order to identify those counties which are more at risk than others. By identifying these counties, resources can be deployed more efficiently. 

The target variable selected was cumulative Covid-19 deaths. 





### Data:

- US county-level census data scraped from the Census Bureau [QuickFacts](https://www.census.gov/quickfacts/fact/table/) page
- Covid-19 county-level data dated 01/18/2021 from the New York Times GitHub [repository](https://github.com/nytimes/covid-19-data)
- Covid-19 county-level data scraped from the CDC [data tracker](https://covid.cdc.gov/covid-data-tracker/#county-view) (this was ultimately not used in the project)




### Tools used:

- BeautifulSoup and Selenium for web scraping (the Selenium-acquired data was ultimately not used)
- Feature engineering, Box-Cox transform and polynomial features
- Linear regression
- Regularization via LASSO and Ridge regression
- Cross validation
- Matplotlib, Seaborn, Plotly for visualization






