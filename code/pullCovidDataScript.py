from bs4 import BeautifulSoup
import requests
import time, os

import math
import pandas as pd
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def isfloat(value_string_reduced):
  try:
    float(value_string_reduced)
    return float(value_string_reduced)
  except ValueError:
    return math.nan

def grabInitialMetric(soup, input_id):
    this_div = soup.find('div', id=input_id)
    this_span = this_div.find('span', id='initialMetric')
    return isfloat(this_span.text)
#     return isfloat(this_span.text.split(" ")[0].replace("<",''))

def grabPerMetric(soup, input_id):
    this_div = soup.find('div', id=input_id)
    sub_div = this_div.find('div', class_='rates')
    per_text = sub_div.text
    line_of_interest = per_text.split("\n")[1].split(" ")    
    while('' in line_of_interest): 
        line_of_interest.remove('')
    return isfloat(line_of_interest[0].replace("(",''))

def grabCovidData(soup):

    county_dict = {}

    svi_span = soup.find('span', id='svi_rank')
    svi_value = isfloat(svi_span.text)
    county_dict['SVI'] = svi_value
        
    ccvi_span = soup.find('span', id='ccvi_score')
    ccvi_value = isfloat(ccvi_span.text)
    county_dict['CCVI'] = ccvi_value

    county_dict['Cases'] = grabInitialMetric(soup, 'cases-timeseries-wrapper')
    county_dict['Cases per 100k'] = grabPerMetric(soup, 'cases-timeseries-wrapper')

    county_dict['Deaths'] = grabInitialMetric(soup, 'deaths-timeseries-wrapper')
    county_dict['Deaths per 100k'] = grabPerMetric(soup, 'deaths-timeseries-wrapper')

    county_dict['Percent Positivity'] = grabInitialMetric(soup, 'positivity-timeseries-wrapper')
    
    county_dict['Testing Volume'] = grabInitialMetric(soup, 'testing-timeseries-wrapper')
    county_dict['Testing Volume per 100k'] = grabPerMetric(soup, 'testing-timeseries-wrapper')

    county_dict['New Hospital Admissions'] = grabInitialMetric(soup, 'hospital-admissions-timeseries-wrapper')
    county_dict['New Hospital Admissions per 100 beds'] = grabPerMetric(soup, 'hospital-admissions-timeseries-wrapper')

    county_dict['Percent Beds Used (Covid)'] = grabInitialMetric(soup, 'hospital-percent-beds-timeseries-wrapper')
    
    county_dict['Percent ICU Beds Used (Covid)'] = grabInitialMetric(soup, 'hospital-percent-icu-beds-timeseries-wrapper')

    return county_dict

def cleanCountyInput(county_string):
    return county_string.replace("County",'').replace("Parish",'').replace("City and Borough",'').replace("Borough",'').replace("Census Area",'').rstrip()

def check_file_written(checkfile, stateFileName):
    checkfile.seek(0)
    for line in checkfile:
        if str(stateFileName) in line:
            return True
    return False


def main():

	chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
	os.environ["webdriver.chrome.driver"] = chromedriver

	county_census_info = pd.read_pickle("../Data/county_census_info.pkl")
	county_census_info.drop('District of Columbia', level='STATE', inplace=True)

	state_dataframes = []
	for state in county_census_info.index.unique(level='STATE'):
	    state_dataframes.append(county_census_info.loc[pd.IndexSlice[:,state],:])


	# open the cdc website and choose the state and county from the drop down menu, then scrape data

	cdc_county_website = "https://covid.cdc.gov/covid-data-tracker/#county-view"

	driver = webdriver.Chrome(chromedriver)
	driver.get(cdc_county_website)

	time.sleep(10)

	list_of_dicts = []
	# list_of_missed_rows = []

	# i = 0
	for state_frame in state_dataframes:
	    # i+=1
	    # if(i > 10): break
	        
	    reduced_state_name = state_frame.index[0][1].replace(" ","")
	    state_file = Path(f"../Data/Covid/{reduced_state_name}.pkl")
	    
	    check_file = open("../Data/Covid/checkFile.txt", "a+")
	    
	    if(check_file_written(check_file, state_file) or state_file.is_file()):
	        print(f"{state_file} already exists, moving on")
	        check_file.close()
	        continue
	              
	    # else scrape the data
	              
	    print(f"Creating file: {state_file}")
	    check_file.write(str(state_file))
	    check_file.write("\n")
	    check_file.close()
	    
	    
	    # j = 0
	    for index, row in state_frame.iterrows():
	        # j+=1
	        # if(j>1): break
	            
	        state_input = index[1]
	        county_input = cleanCountyInput(index[0])

	        print(state_input, county_input)

	        select = Select(driver.find_element_by_id('list_select_state'))
	        select.select_by_visible_text(state_input)

	        time.sleep(1)

	        select = Select(driver.find_element_by_id('list_select_county'))
	        select.select_by_visible_text(county_input)

	        time.sleep(20) # was 15

	        # scrape data from the page

	        soup = BeautifulSoup(driver.page_source, "lxml")

	        county_dict = grabCovidData(soup)
	        county_dict['COUNTY'] = index[0]
	        county_dict['STATE'] = index[1]        
	        list_of_dicts.append(county_dict) 

	        
	    # done with counties in the state, now convert to a dataframe and save it
	        
	    state_county_covid_info_df = pd.DataFrame(list_of_dicts)
	    state_county_covid_info_df.set_index(['COUNTY','STATE'],inplace=True)
	    state_county_covid_info_df

	    state_county_covid_info_df.to_pickle(state_file)
	    print(f"Finished file: {state_file}")

	    
	# close driver at end
	driver.close()

	print('Done')


main()
