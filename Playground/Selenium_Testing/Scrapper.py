import os

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta
from seleniumwire import webdriver                      
from selenium.webdriver.chrome.service import Service
def rendering(url):
        service = Service(executable_path='geckodriver.exe')
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        # change '/usr/local/bin/chromedriver' to the path 
        # from you got when you ran 'which chromedriver'
        driver = webdriver.Firefox(service=service,options=options)
        #Chrome('C:\Users\Gizmodget\Documents\Repositories\4883-SoftwareTools-Ellerkamp\Playground\Selenium_Testing\geckodriver') # run ChromeDriver
        driver.get(url)                                          # load the web page from the URL
        time.sleep(3)                                            # wait for the web page to load
        render = driver.page_source                              # get the page source HTML
        driver.quit()                                            # quit ChromeDriver
        return render                                            # return the page source HTML
def scrape_airport_weather(station, start_date, end_date):
    
    # make a new directory for each airport that you scrape
    # data for, to keep files separate and organized
    if not os.path.exists(station):
        os.mkdir(station) 
        
    # search URL that can be formatted to find the web page for any airport on any observation date     
    search_url = 'http://www.wunderground.com/history/daily/{}/date/{}-{}-{}' 
    
    # csv file name that can be formatted for any airport and any year
    outfile = '{}/{}_{}.csv'.format(station, station, start_date.year)
    
    # if the csv file does not exist, write, if it does exist, append
    if not os.path.exists(outfile):
        mode = 'w'
    else:
        mode = 'a'
        
    with open(outfile, mode) as f:
        # write column headers for each paramter into the file for later use
        if mode == 'w':
            f.write('date,actual_high_temp,histavg_high_temp,record_high_temp,'
                    'actual_low_temp,histavg_low_temp,record_low_temp,'
                    'actual_avg_temp,histavg_avg_temp,record_avg_temp,'
                    'actual_precip,histavg_precip,record_precipitation\n')
    
        # while loop continues until it reaches the given end date
        while start_date != end_date:
            
            # format the search URL for the given airport and observation date 
            format_search_url = search_url.format('K'+station,
                                                  start_date.year,
                                                  start_date.month,
                                                  start_date.day)
        
            wunderground_page = rendering(format_search_url)
        
            wunderground_soup = BeautifulSoup(wunderground_page, 'html.parser')
            soup_container = wunderground_soup.find('lib-city-history-summary')
            soup_data = soup_container.find_all('tbody', class_='ng-star-inserted')
        
            row = []
            for i, dat in enumerate(soup_data):
                # loops through High Temp, Low Temp, etc.
                for j, d in enumerate(dat.find_all('tr', class_='ng-star-inserted')):
                    # loops through Actual, Historic Avg., Record
                    for k in d.find_all('td', class_='ng-star-inserted'):
                        tmp = k.text
                        tmp = tmp.strip('  ') # remove any extra spaces
                        
                        row.append(tmp)

            # write the observation date into the file
            f.write('{}-{}-{},'.format(start_date.year, start_date.month, start_date.day))
            # write just the temperature and precipitation data into the file
            f.write(','.join(row[:12]))
            # new line, in case you want to append more rows to the same file later on
            f.write('\n')

            start_date += timedelta(days=1) # go to next date, i.e., next URL


station = 'CHO'
start_date = datetime(year=2020, month=1, day=1)
end_date = datetime(year=2020, month=1, day=3)

scrape_airport_weather(station, start_date, end_date)