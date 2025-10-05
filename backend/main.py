import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from harmony import BBox

def main():
    # load .env for token
    load_dotenv()
    token = os.getenv("EARTHDATA_TOKEN")

    # # Harmony endpoint
    # url = "https://harmony.earthdata.nasa.gov/async"

    ## vars for API requests   
    # Default Parameters to show data before user input        
    latitude = 38.8951
    longitude = -77.0364
    date = "2024-12-31"
    start_time = "00:00:00" # default 12am
    stop_time = "23:59:59" # default 11:59pm

    ## GET requests
    # GET precipitation via GPM_3IMERGHH v07 via Harmony
    def get_precip (date, latitude, longitude, start_time, stop_time, token):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            # "bbox": f"{longitude - 0.05}, {latitude - 0.05}, {longitude + 0.05}, {latitude + 0.05}",
            "datetime": f"{date}T{start_time}Z/{date}T{stop_time}Z",
            "parameter-name": "precipitationCal"
        }

        url = "https://harmony.earthdata.nasa.gov/ogc-api-edr/1.1.0/collections/C2723754847-GES_DISC/cube"

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        job_id = data.get("jobID")
        print(json.dumps(response.json(), indent=2))

        jobs_url = f"https://harmony.earthdata.nasa.gov/jobs/{job_id}"
        response = requests.get(jobs_url, headers=headers)
        print(json.dumps(response.json(), indent=2))
    
    print("Fetching IMERG data. Thank you, NASA ❤️") 
    get_precip(date, latitude, longitude, start_time, stop_time, token)


if __name__ == "__main__":
    main()