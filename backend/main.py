import json
import requests

def main():
    
    ## vars for API requests   
    # Default Parameters to show data before user input        
    station = "KDCA"
    year = "2024"
    month = "12"
    day = "5"

    # GET weather data (historical FAA METAR observations) via Mesonet API  
    metar_url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
    params = {
        "station": station,
        "data": "station,valid,tmpf,relh,sknt,p01i",
        "year1": year,
        "month1": month,
        "day1": day,
        "year2": year,
        "month2": month,
        "day2": day,
        "tz": "UTC",
        "format": "onlycomma"
    }

    print("Fetching METAR data ✈️") 
    res = requests.get(metar_url, params=params)
    res.raise_for_status()
    metar_data = res.text

    print("METAR data:", metar_data)

if __name__ == "__main__":
    main()