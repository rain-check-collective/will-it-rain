import asyncio
import httpx

# GET precipitation via GPM_3IMERGHH v07 via Harmony
async def get_precip (date, latitude, longitude, start_time, stop_time, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = [
        ("subset", f"lon({longitude-0.1}:{longitude+0.1})"),
        ("subset", f"lat({latitude-0.1}:{latitude+0.1})"),
        ("subset", f'time("{date}T{start_time}Z":"{date}T{stop_time}Z")'),
        ("parameter-name", "precipitationCal"),
        # ("f", "application/x-netcdf4")
    ]
    
    precip_url = "https://harmony.earthdata.nasa.gov/ogc-api-edr/1.1.0/collections/C2723754847-GES_DISC/cube"

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(precip_url, headers=headers, params=params)
            if res.status_code in (302, 303):
                job_url = res.headers.get("Location")
                if job_url.startswith('/'):
                    job_url =  f"https://harmony.earthdata.nasa.gov{job_url}"
                print("Job submitted:", job_url)
                return job_url
            
            res.raise_for_status()

            data = res.json()
            job_id = data.get("jobID")
            job_url = f"https://harmony.earthdata.nasa.gov/jobs/{job_id}"
            return job_url
        
        except httpx.HTTPStatusError as e:
            print("EDR error body: ", e.response.text)
            raise

# async def precip_poll_job(job_url, headers):
#     async with httpx.AsyncClient() as client:
#         while True:
#             res = await client.get(job_url, headers=headers)
#             info = res.json()
#             status = info.get("status")
#             granules = info.get("granules")

#             print(f"Job status: {status}, granules: {granules}")

#             if status == "successful" and granules == 0:
#                 print("Job completed but found 0 granules.")
#                 print("Full response:", info)
#                 return info

#             if status in {"successful", "failed", "canceled"}:
#                 return info
            
#             await asyncio.sleep(2)

async def precip_poll_job(job_url, headers):
    async with httpx.AsyncClient() as client:
        while True:
            res = await client.get(job_url, headers=headers)
            info = res.json()
            status = info.get("status")
            granules = info.get("numInputGranules")
            
            print(f"Job status: {status}, granules: {granules}")
            
            if status in {"successful", "failed", "canceled"}:
                # Print the full response to see error messages
                print("\n=== FULL JOB RESPONSE ===")
                import json
                print(json.dumps(info, indent=2))
                print("=========================\n")
                
                # Check for errors or messages
                if "errors" in info:
                    print("Errors:", info["errors"])
                if "message" in info:
                    print("Message:", info["message"])
                
                return info
            
            await asyncio.sleep(2)