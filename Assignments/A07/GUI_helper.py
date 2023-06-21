""" 
Description:
    This is an example gui that allows you to enter the appropriate parameters to get the weather from wunderground.
TODO:
    - You will need to change the text input boxes to drop down boxes and add the appropriate values to the drop down boxes.
    - For example the month drop down box should have the values 1-12.
    - The day drop down box should have the values 1-31.
    - The year drop down box should have the values ??-2023.
    - The filter drop down box should have the values 'daily', 'weekly', 'monthly'.
"""
import PySimpleGUI as sg      
import json

def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    from datetime import datetime
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day':datetime.now().day,
        'month':datetime.now().month,
        'year':datetime.now().year
    }

def buildWeatherURL(month=None, day=None, year=None, airport=None, filter=None):
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month,current_day,current_year = currentDate('tuple')
    
    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year
    
    # Create the gui's layout using text boxes that allow for user input without checking for valid input
    List_of_Days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    List_of_Months = [1,2,3,4,5,6,7,8,9,10,11,12]
    List_of_Years = list(range(2000,2024))
    with open('./Assignments/A07/Airport_Codes.json') as f:
        Airport_Data = json.load(f)
        Airport_Codes = []
        for data in Airport_Data:
            #print(data["icao"])
            Airport_Codes.append(data["icao"]  + ", " + data["name"])
#        print(Airport_Codes) 
    List_of_Filters = ['daily', 'weekly', 'monthly']
    layout = [
        [sg.Text('Month')],[sg.Combo(List_of_Months,1)],
        [sg.Text('Day')],[sg.Combo(List_of_Days,1)],
        [sg.Text('Year')],[sg.Combo(List_of_Years, 2012)],
        [sg.Text('Code')],[sg.Combo(Airport_Codes)],
        [sg.Text('Daily / Weekly / Monthly')],[sg.Combo(List_of_Filters, 'daily')],
        [sg.Submit(), sg.Cancel()]
    ]      

    window = sg.Window('Get The Weather', layout)    

    event, values = window.read()
    window.close()
        
    month = values[0]
    day = values[1]
    year = values[2]
    code = values[3][:4]
    filter = values[4]

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, Code: {code}, Filter: {filter}")

    search_url = 'https://www.wunderground.com/history/{}/{}/date/{}-{}-{}'
    format_search_url = search_url.format(filter,code,
                                                  year,
                                                  month,
                                                  day)
    return format_search_url
    # return the URL to pass to wunderground to get appropriate weather data

if __name__=='__main__':
    print(buildWeatherURL())