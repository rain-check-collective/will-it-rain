
import json
import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

def main():
    # Load .env for token
    load_dotenv()
    token = os.getenv("EARTHDATA_TOKEN")

    latitude = 38.8951
    longitude = -77.0364
    date = "2024-12-31"
    start_time = "00:00:00"
    stop_time = "23:59:59"

    def get_precip(date, latitude, longitude, start_time, stop_time, token):
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "datetime": f"{date}T{start_time}Z/{date}T{stop_time}Z",
            "parameter-name": "precipitationCal"
        }

        url = "https://harmony.earthdata.nasa.gov/ogc-api-edr/1.1.0/collections/C2723754847-GES_DISC/cube"

        print("Submitting job to Harmony API...")
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        job_id = data.get("jobID")

        if not job_id:
            print("❌ No jobID returned. Response:")
            print(json.dumps(data, indent=2))
            return

        print(f"✅ Job submitted successfully. jobID: {job_id}")

        # Poll job status until it's done
        jobs_url = f"https://harmony.earthdata.nasa.gov/jobs/{job_id}"
        status = None

        while True:
            time.sleep(5)
            job_response = requests.get(jobs_url, headers=headers)
            job_data = job_response.json()
            status = job_data.get("status")
            print(f"Job status: {status}")

            if status in ["successful", "failed", "canceled"]:
                break

        if status != "successful":
            print("❌ Job failed or was canceled.")
            print(json.dumps(job_data, indent=2))
            return

        # Get result link
        links = job_data.get("links", [])
        result_links = [l["href"] for l in links if l.get("rel") == "data"]
        if not result_links:
            print("⚠️ No result links found.")
            return

        result_url = result_links[0]
        print(f"✅ Fetching data from: {result_url}")
        result = requests.get(result_url)
        print("✅ Final Data Retrieved Successfully:")
        print(result.text[:1000])  # print first 1000 chars

    print("Fetching IMERG data from NASA Harmony ❤️")
    get_precip(date, latitude, longitude, start_time, stop_time, token)

if __name__ == "__main__":
    main()
