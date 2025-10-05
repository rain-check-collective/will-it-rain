import pandas as pd
import requests

from io import StringIO

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

    ## data handling via pandas and StringIO
    # DataFrame to hold API values
    df = pd.read_csv(StringIO(metar_data))

    # Replace missing values ('M') with NaN (not a number)
    df.replace('M', pd.NA, inplace=True)

    # Convert returned API values to numbers so we can do math
    converted_vals = ['tmpf', 'relh', 'sknt', 'p01i']
    for val in converted_vals:
        df[val] = pd.to_numeric(df[val], errors='coerce')

    # Filter out missing values
    df_precip = df[df['p01i'].notna()]
    df_temp = df[df['tmpf'].notna()]
    df_wind = df[df['sknt'].notna()]
    df_relh = df[df['relh'].notna()]

if __name__ == "__main__":
    main()