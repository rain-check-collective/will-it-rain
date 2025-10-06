# Will It Rain
## Project Overview
Rain Check Collective's project for the 2025 NASA Space App Challenge hackathon. This project was built in response to the Will It Rain on My Parade? challenge: https://www.spaceappschallenge.org/2025/challenges/will-it-rain-on-my-parade/?tab=details

## Dataset Used
- Historical FAA METAR via Iowa State Mesonet https://mesonet.agron.iastate.edu/api/
- Retrieved: station, datetime (param: valid), ambient temperature (param: tmpf), relative humidity (param: relh), windspeed (param: sknt), precipitation (param: p01i)

### Why Mesonet instead of NASA Earthdata?
The 2025 Space Apps Challenge coincided with the October 2025 federal government shutdown. During Day One of the hackathon, our attempts to retrieve data from NASA's Earthdata Harmony API endpoints consistently returned 0 granules or job failures across multiple collection IDs and query parameters.

Given time constraints and API reliability issues, the team pivoted to FAA METAR data via Iowa State University's Environmental Mesonet archive. This source provides comprehensive historical aviation weather observations and is maintained independently of federal services, allowing us to proceed with implementation.

## Tech Stack
Built in Python with HTML/CSS UI layer.

### Tools Used:
- FastAPI (routing to connect front end to backend)
- pandas (CSV parsing and missing-value handling)
- pydantic (works with FastAPI for data validation on routes)
- Requests (API calls)
- StringIO (allows pandas to parse streamed CSV returned via API as if it were a file)
- uvicorn (server to run FastAPI)

## Current Status
- ✅ API integration with Iowa State Mesonet
- ✅ Data parsing and cleaning (handles missing values)
- 🚧 Multi-year data retrieval
- 🚧 Percentage calculations for weather likelihood
- 🚧 Frontend integration

## Contributors
- cynthiablack - Backend/API integration
- emmebravo - Full Stack
- earlytomorrow - Documentation
- asharify - Testing, Troubleshooting, and Snarl Untangling
- Claude / ChatGPT - debugging