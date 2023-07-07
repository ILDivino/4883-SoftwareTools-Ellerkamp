"""
Michael Ellerkamp
Assignment 08: using FastAPI with covid data.
We are to build an API using FastAPI and covid data. Certain endpoints are required and proper commenting is important.
A lion's share of the code was provided by the instructor.

The format of the data file for reference:
# 	Column 	Description
0 	Date_reported 	date in yyyy-mm-dd format
1 	Country_code 	A unique 2 digit country code
2 	Country 	Name of the country
3 	WHO_region 	World Health Organization region
4 	New_cases 	Number of new cases on this date
5 	Cumulative_cases 	Cumulative cases up to this date
6 	New_deaths 	Number of new deaths on this date
7 	Cumulative_deaths 	Cumulative deaths up to this date
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import csv
import datetime


description = """🚀
## 4883 Software Tools
### Where awesomeness happens
"""


app = FastAPI(

    description=description,

)

db = []

# Open the CSV file
with open('./Assignments/A08/data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    i = 0
    # Read each row in the CSV file
    for row in reader:
        if i == 0:
            i += 1
            continue
        db.append(row)


def getUniqueCountries():
    global db
    countries = {}

    for row in db:
#        print(row)
        if not row[2] in countries:
            countries[row[2]] = 0

    return list(countries.keys())

def getUniqueWhos():
    global db
    whos = {}

    for row in db:
#        print(row)
        if not row[3] in whos:
            whos[row[3]] = 0
   
    return list(whos.keys())
"""
getDeaths will have 3 loops.
/deaths/ loop
/region loop
/country loop
Year is only a modifier for region and country
Country and Region do not mix in the calls.
"""
def getDeaths(Region, Country, Year):
    global db
    deaths = 0
    print(Region, Country, Year)
    #/deaths/ call with no parameters
    if Region == "ALL" and Country == "ALL" and Year == -1:
        for row in db:
            deaths += int(row[6])
    # Region loop
    elif(Region != "ALL"):
        for row in db:
            #if the region matches the filter continue
            if Region == row[3]:
                #if no year is set then add deaths
                if(Year == -1):
                    deaths += int(row[6])
                #if the year is set then make sure the row's year matches the target year
                elif(Year == int(row[0][:4])):
                    deaths += int(row[6])
    #country loop
    elif(Country != "ALL"):
            for row in db:
                #if the country matches the filter continue
                if Country == row[2]:
                    #if no year is set then add deaths
                    if(Year == -1):
                        deaths += int(row[6])
                    #if the year is set then make sure the row's year matches the target year
                    elif(Year == int(row[0][:4])):
                        deaths += int(row[6])

    return deaths

"""
getCases will have 3 loops.
/cases/ loop
/region loop
/country loop
Year is only a modifier for region and country
Country and Region do not mix in the calls.
"""
def getCases(Region, Country, Year):
    global db
    cases = 0
    print(Region, Country, Year)
    #/cases/ call with no parameters
    if Region == "ALL" and Country == "ALL" and Year == -1:
        for row in db:
            cases += int(row[4])
    # Region loop
    elif(Region != "ALL"):
        for row in db:
            #if the region matches the filter continue
            if Region == row[3]:
                #if no year is set then add cases
                if(Year == -1):
                    cases += int(row[4])
                #if the year is set then make sure the row's year matches the target year
                elif(Year == int(row[0][:4])):
                    cases += int(row[4])
    #country loop
    elif(Country != "ALL"):
            for row in db:
                #if the country matches the filter continue
                if Country == row[2]:
                    #if no year is set then add cases
                    if(Year == -1):
                        cases += int(row[4])
                    #if the year is set then make sure the row's year matches the target year
                    elif(Year == int(row[0][:4])):
                        cases += int(row[4])

    return cases
"""
Two scenarios.
1. no date is input so I just need to look at total deaths.
2. Dates are used so now I have to add deaths by day.
"""
def getMaxDeaths(Start_Date, End_Date):
    global db
    Max_Deaths = {}
    Peak_Deaths = 0
    format = '%Y-%m-%d'

#scenario 1, I know that if one date is None both are None due to my checking in the @app
    if(Start_Date is None):
        for row in db:
            if int(row[7]) > Peak_Deaths:
                Peak_Deaths = int(row[7])
        for row in db:
            if int(row[7]) == Peak_Deaths and not row[2] in Max_Deaths:
                Max_Deaths[row[2]] = Peak_Deaths
        return Max_Deaths
#scenario 2, summing up all the new deaths between the start and end date and then comparing countries.
    else:
        startdate = datetime.datetime.strptime(Start_Date, format)
        enddate = datetime.datetime.strptime(End_Date, format)
        for row in db:
            #the date for the row is within my range
            if datetime.datetime.strptime(row[0], format) >= startdate and datetime.datetime.strptime(row[0], format) <= enddate:
                #new instance of a country
                if not row[2] in Max_Deaths:
                    Max_Deaths[row[2]] = int(row[6])
                else:
                    Max_Deaths[row[2]] += int(row[6])
        #now to check Max_Deaths for the highest contenders and return them
        maximum = max(Max_Deaths, key=Max_Deaths.get)  # Just use 'min' instead of 'max' for minimum.
        return(maximum, Max_Deaths[maximum])
"""
Two scenarios.
1. Unlike max deaths, more processing is required for min death without year scope.
2. Dates are used so now I have to add deaths by day.
"""
def getMinDeaths(Start_Date, End_Date):
    global db
    Min_Deaths = {}
    Peak_Deaths = 0
    format = '%Y-%m-%d'

#scenario 1, I know that if one date is None both are None due to my checking in the @app
    if(Start_Date is None):
        for row in db:
            if not row[2] in Min_Deaths:
                Min_Deaths[row[2]] = int(row[6])
            else:
                Min_Deaths[row[2]] += int(row[6])
        #now to check Min_Deaths for the highest contenders and return them
        minimum = min(Min_Deaths, key=Min_Deaths.get)  # Just use 'min' instead of 'max' for minimum.
        return(minimum, Min_Deaths[minimum])
#scenario 2, summing up all the new deaths between the start and end date and then comparing countries.
    else:
        startdate = datetime.datetime.strptime(Start_Date, format)
        enddate = datetime.datetime.strptime(End_Date, format)
        for row in db:
            #the date for the row is within my range
            if datetime.datetime.strptime(row[0], format) >= startdate and datetime.datetime.strptime(row[0], format) <= enddate:
                #new instance of a country
                if not row[2] in Min_Deaths:
                    Min_Deaths[row[2]] = int(row[6])
                else:
                    Min_Deaths[row[2]] += int(row[6])
        #now to check Min_Deaths for the highest contenders and return them
        minimum = min(Min_Deaths, key=Min_Deaths.get)  # Just use 'min' instead of 'max' for minimum.
        return(minimum, Min_Deaths[minimum])
    
def getAvg_Deaths():
    global db
    countries = {}
    count = {}

    for row in db:
#        print(row)
        if not row[2] in countries:
            countries[row[2]] = int(row[6])
            count[row[2]] = 1
        else:
            countries[row[2]] += int(row[6])
            count[row[2]] += 1
    for items in countries:
        countries[items] = int(countries[items]/count[items])
    return countries

@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/countries/")
async def countries():
    """
    This method will return all unique countries.
    - **Params:**
      - None
    - **Returns:**
      - (list) : All Unique Countries

    #### Example 1:

    [http://localhost:8000/countries/](http://localhost:8000/countries/)

    #### Response 1:

        "countries": [
    "Afghanistan",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    ...
    """

    return {"countries":getUniqueCountries()}

@app.get("/regions/")
async def regions():
    """
    This method will return all unique regions.
    - **Params:**
      - None
    - **Returns:**
      - (list) : All Unique Regions

    #### Example 1:

    [http://localhost:8000/regions/](http://localhost:8000/regions/)

    #### Response 1:

      "regions": [
    "EMRO",
    "EURO",
    "AFRO",
    "WPRO",
    "AMRO",
    "SEARO",
    "Other"
    """

    return {"regions":getUniqueWhos()}

@app.get("/deaths/")
async def deaths(Region: str or None = None, Country: str or None = None, Year: int or None = None):
    """
    This method will return all deaths and can be filtered.
    - **Params:**
      - Region (str) : WHO Region Name
      - Country (str) : Country Name
      - Year (Int) : Target Year for the search.
    - **Returns:**
      - (int) : Total Deaths, if no parameters are used
      - (int) : Total Deaths for a country
      - (int) : Total Deaths for a country within a select year.
      - (int) : Total Deaths for a region
      - (int) : Total Deaths for a region within a select year.

    #### Example 1:

    [http://localhost:8000/deaths/](http://localhost:8000/deaths/)

    #### Response 1:
    {
        "deaths": 6945714
    }
    #### Example 2:
    [http://localhost:8000/deaths/?Region=EMRO](http://localhost:8000/deaths/?Region=EMRO)

    ### Response 2:
    {
         "deaths": 351329
    }
    """    #input validation
    try:
        #Country or Region can be used but not both in a single call
        if isinstance(Country, str) and isinstance(Region, str):
            return {"error": "Region and Country can not be used at same time."}
        #Year cannot be by itself
        elif Year is not None and Region is None and Country is None:
            return {"error": "Year must be used with a Country or Region."}
        #if year is None then I use -1 as a placeholder else year must be within 2020 and 2023
        if Year is None:
            Year = -1
        elif Year < 2020 and Year > 2023:
            return {"error": "Invalid Year provided. Year must be [2020 - 2023]"}

        #ALL is a token for no region listed and then region is checked to make sure it is actually a region.
        if Region is None:
            Region = "ALL"
        elif isinstance(Region, str):
            if Region not in getUniqueWhos():
                return {"error": "Invalid Region provided. Region must be a WHO region"}
        else:
            return {"error": "Invalid Region provided. Region must be a string"}

        #ALL is a token for no country and then country is checked to make sure it is a country
        if Country is None:
            Country = "ALL"
        elif isinstance(Country, str):
            if Country not in getUniqueCountries():
                return {"error": "Invalid Country provided."}
        else:
            return {"error": "Invalid Country provided. Country must be a string"}
    #a defaultish error in case I missed something
    except:
        return {"error": "Invalid input provided."}

    return {"deaths":getDeaths(Region, Country, Year)}

@app.get("/cases/")
async def cases(Region: str or None = None, Country: str or None = None, Year: int or None = None):
    """
    This method will return all cases and can be filtered down.
    - **Params:**
      - Region (str) : WHO Region Name
      - Country (str) : Country Name
      - Year (Int) : Target Year for the search.
    - **Returns:**
      - (int) : Total Cases, if no parameters are used
      - (int) : Total Cases for a country
      - (int) : Total Cases for a country within a select year.
      - (int) : Total Cases for a region
      - (int) : Total Cases for a region within a select year.

    #### Example 1:

    [http://localhost:8000/cases/](http://localhost:8000/cases/)

    #### Response 1:
    {
        cases	768187096
    }
    #### Example 2:
    [http://localhost:8000/cases/?Region=EMRO](http://localhost:8000/cases/?Region=EMRO)

    ### Response 2:
    {
         cases	23382124
    }
    """    
    #input validation
    try:
        #Country or Region can be used but not both in a single call
        if isinstance(Country, str) and isinstance(Region, str):
            return {"error": "Region and Country can not be used at same time."}
        #Year cannot be by itself
        elif Year is not None and Region is None and Country is None:
            return {"error": "Year must be used with a Country or Region."}
        #if year is None then I use -1 as a placeholder else year must be within 2020 and 2023
        if Year is None:
            Year = -1
        elif Year < 2020 and Year > 2023:
            return {"error": "Invalid Year provided. Year must be [2020 - 2023]"}

        #ALL is a token for no region listed and then region is checked to make sure it is actually a region.
        if Region is None:
            Region = "ALL"
        elif isinstance(Region, str):
            if Region not in getUniqueWhos():
                return {"error": "Invalid Region provided. Region must be a WHO region"}
        else:
            return {"error": "Invalid Region provided. Region must be a string"}

        #ALL is a token for no country and then country is checked to make sure it is a country
        if Country is None:
            Country = "ALL"
        elif isinstance(Country, str):
            if Country not in getUniqueCountries():
                return {"error": "Invalid Country provided."}
        else:
            return {"error": "Invalid Country provided. Country must be a string"}
    #a defaultish error in case I missed something
    except:
        return {"error": "Invalid input provided."}

    return {"cases":getCases(Region, Country, Year)}

@app.get("/maxdeaths/")
async def maxdeaths(Start_Date: str or None = None, End_Date: str or None = None):
    """
    This method will return Country with the most deaths
    - **Params:**
      - Start_Date (str) : Lower bound of the date range
      - End_Date (str) : Upper bound of the date range (inclusive)
    - **Returns:**
      - (str) : Country with the most deaths
      - (int) : the number of deaths

    #### Example 1:

    [http://localhost:8000/maxdeaths/](http://localhost:8000/maxdeaths/)

    #### Response 1:
    {
        United States of America	1127152
    }
    #### Example 2:
    [http://localhost:8000/maxdeaths/?Start_Date=2020-1-1&End_Date=2021-1-1](http://localhost:8000/maxdeaths/?Start_Date=2020-1-1&End_Date=2021-1-1)

    ### Response 2:
     "maxdeaths": [
        "United States of America",
        355767
    ]
    """

    Low_Bound = datetime.datetime(2020,1,1)
    High_Bound = datetime.datetime(2023,6,21)
    #if a value is plugged into on date and not the other this will produce an error.
    if (Start_Date is not None and End_Date is None) or (End_Date is not None and Start_Date is None):
        return {"error": "Either both dates must be entered or no dates."}
    elif(Start_Date is not None) and (End_Date is not None):
        try:
            format = '%Y-%m-%d'
            # convert from string format to datetime format
            startdate = datetime.datetime.strptime(Start_Date, format)
            enddate = datetime.datetime.strptime(End_Date, format)
        except:
            return {"error": "Invalid date format. YYYY-MM-DD"}
        #start must be before the end.
        if (startdate > enddate):
            return {"error": "Invalid date provided. Start date must be before the End date"}
        #dates must be within the scope of the data.
        elif startdate < Low_Bound or enddate > High_Bound:
            return {"error": "Dates not in range. Dates must be between [2020 - 2023]"}
    return {"maxdeaths":getMaxDeaths(Start_Date, End_Date)}
    
@app.get("/mindeaths/")
async def mindeaths(Start_Date: str or None = None, End_Date: str or None = None):
    """
    This method will return Country with the least deaths
    - **Params:**
      - Start_Date (str) : Lower bound of the date range
      - End_Date (str) : Upper bound of the date range (inclusive)
    - **Returns:**
      - (str) : Country with the least deaths
      - (int) : the number of deaths

    #### Example 1:

    [http://localhost:8000/mindeaths/](http://localhost:8000/mindeaths/)

    #### Response 1:
        0	"Democratic People's Republic of Korea"
        1	0
    #### Example 2:
    [http://localhost:8000/mindeaths/?Start_Date=2020-1-1&End_Date=2021-1-1](http://localhost:8000/mindeaths/?Start_Date=2020-1-1&End_Date=2021-1-1)

    ### Response 2:
        mindeaths	
        0	"American Samoa"
        1	0
    """

    Low_Bound = datetime.datetime(2020,1,1)
    High_Bound = datetime.datetime(2023,6,21)
    #if a value is plugged into on date and not the other this will produce an error.
    if (Start_Date is not None and End_Date is None) or (End_Date is not None and Start_Date is None):
        return {"error": "Either both dates must be entered or no dates."}
    elif(Start_Date is not None) and (End_Date is not None):
        try:
            format = '%Y-%m-%d'
            # convert from string format to datetime format
            startdate = datetime.datetime.strptime(Start_Date, format)
            enddate = datetime.datetime.strptime(End_Date, format)
        except:
            return {"error": "Invalid date format. YYYY-MM-DD"}
        #start must be before the end.
        if (startdate > enddate):
            return {"error": "Invalid date provided. Start date must be before the End date"}
        #dates must be within the scope of the data.
        elif startdate < Low_Bound or enddate > High_Bound:
            return {"error": "Dates not in range. Dates must be between [2020 - 2023]"}
    return {"mindeaths":getMinDeaths(Start_Date, End_Date)}

@app.get("/avg_deaths/")
async def avg_deaths():
    """
    This method will return the average number of deaths. Deaths / Country
    - **Params:**
      - None
    - **Returns:**
      - list(int) : the total number of deaths per country. deaths/(time instances) per country

    #### Example 1:

    [http://localhost:8000/avg_deaths/](http://localhost:8000/avg_deaths/)

    #### Response 1:
        "Malta": 0,
        "Marshall Islands": 0,
        "Martinique": 0,
        "Mauritania": 0,
        "Mauritius": 0,
        "Mayotte": 0,
        "Mexico": 264,
        "Micronesia (Federated States of)": 0,
        "Monaco": 0,
        "Mongolia": 1,
        "Montenegro": 2,
    """

    return {"avg_deaths":getAvg_Deaths()}

if __name__ == "__main__":
    uvicorn.run("Main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True) #host="127.0.0.1"