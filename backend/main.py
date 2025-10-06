import pandas as pd
import requests

from io import StringIO
from .calculations import (
    calc_precip_average,
    calc_high_temp_average,
    calc_low_temp_average,
    calc_wind_average,
    calc_humidity_average
)

# Main method with default values 
def main(station="KDCA", year="2024", month="12", day="5"):
    # Set number of years to collect for climate averages
    years_back = 10

    # Empty array to capture API response data
    all_data = []

    # GET weather data (historical FAA METAR observations) via Mesonet API  
    print("Fetching METAR data ✈️") 

    # Fetch API data for number of years set in years_back
    for i in range(years_back + 1):
        metar_url = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
        target_year = int(year) - i
        params = {
            "station": station,
            "data": "station,valid,tmpf,relh,sknt,p01i",
            "year1": str(target_year),
            "month1": month,
            "day1": day,
            "year2": str(target_year),
            "month2": month,
            "day2": day,
            "tz": "UTC",
            "format": "onlycomma"
        }

        res = requests.get(metar_url, params=params)
        res.raise_for_status()
        all_data.append(res.text)      

    # Combine API response data
    metar_data = all_data[0]
    for csv_text in all_data[1:]:
        lines = csv_text.split('\n')
        metar_data += '\n' + '\n'.join(lines[1:])

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

    # Calculate percentages for cards
    rain_pct = calc_precip_average(df_precip)
    hot_pct = calc_high_temp_average(df_temp)
    cold_pct = calc_low_temp_average(df_temp)
    windy_pct = calc_wind_average(df_wind)
    humid_pct = calc_humidity_average(df_relh)

    return {
        "rain": rain_pct,
        "heat": hot_pct,
        "cold": cold_pct,
        "wind": windy_pct,
        "humidity": humid_pct
    }

if __name__ == "__main__":
    main()