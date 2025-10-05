import json
import requests

def main():
    
    ## vars for API requests   
    # Default Parameters to show data before user input        
    station = "KDCA"
    date = "2024-12-31"

    # GET weather data via FAA METAR API  
    metar_url = "https://aviationweather.gov/api/data/metar"
    params = {
        "ids": station,
        "date": date,
        "format": "json"
    }

    print("Fetching METAR data ✈️") 
    res = requests.get(metar_url, params=params)
    res.raise_for_status()
    metar_data = res.json()

    print("METAR data:", metar_data)

if __name__ == "__main__":
    main()