import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# import project methods
from get_precip import get_precip, precip_poll_job

def main():
    # load .env for token
    load_dotenv()
    token = os.getenv("EARTHDATA_TOKEN")

    print("Token loaded?", bool(token))
    import requests
    print("GES DISC:", requests.get("https://harmony.earthdata.nasa.gov/ogc-api-edr/1.1.0/collections/C2723754847-GES_DISC/cube").status_code)

    # headers for API calls
    headers = {
        "Authorization": f"Bearer {token}"
    }

    ## vars for API requests   
    # Default Parameters to show data before user input        
    latitude = 13.7563
    longitude = 100.5018
    date = "2023-07-15"
    start_time = "00:00:00" # default 12am
    stop_time = "01:00:00" # default 1am

    ## GET requests    
    print("Fetching IMERG data. Thank you, NASA ❤️") 
    job_url = asyncio.run(get_precip(date, latitude, longitude, start_time, stop_time, token))
    info = asyncio.run(precip_poll_job(job_url, headers))
    print("Final status:", info.get("status"))

if __name__ == "__main__":
    main()