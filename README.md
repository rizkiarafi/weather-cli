# CLI Weather Forecast Tool

A command-line interface (CLI) Python application that detects your geographic location via your IP address and displays a 5-day weather forecast (updated every 3 hours) in a clean, tabular format.

## Features

- **Automated IP Geolocation**: Detects your public IPv6 address and queries the `iplocate.io` API to retrieve your exact latitude and longitude.
- **5-Day / 3-Hour Weather Forecast**: Queries the OpenWeatherMap API to fetch a detailed 5-day forecast with data points recorded every 3 hours (total of 40 data points).
- **Representative Daily Forecasts**: Extracts 5 representative forecast intervals (spaced 24 hours apart) from the 40 forecast data points to construct a daily overview.
- **Intelligent Caching System**: 
  - Geo-location and IP data are cached locally to minimize API roundtrips.
  - Weather forecast data is cached for **1 hour (3600 seconds)**. 
  - If you change networks or your IP changes, the cache is automatically invalidated and refreshed.
- **Tabular Display**: Uses `pandas` to format and present the date, weather conditions, temperature, and humidity clearly.

---

## File Structure

- [weather_app.py](file:///F:/Dokumenku/AI%20Roadmap/python-cli/weather-cli/weather_app.py): The main entry point of the CLI application. It fetches the forecast data, parses the representative daily intervals, and prints the data table.
- [weather_data.py](file:///F:/Dokumenku/AI%20Roadmap/python-cli/weather-cli/weather_data.py): The core data module. Handles IP fetching, iplocate.io geo-lookup, caching (writing/reading JSON cache files), and calling the OpenWeatherMap API.
- [requirements.txt](file:///F:/Dokumenku/AI%20Roadmap/python-cli/weather-cli/requirements.txt): Lists all required external libraries.
- [.env](file:///F:/Dokumenku/AI%20Roadmap/python-cli/weather-cli/.env): Configuration file containing your secret API keys (ignored by git).
- [.env.example](file:///F:/Dokumenku/AI%20Roadmap/python-cli/weather-cli/.env.example): Template showing the environment variables needed.

---

## Installation & Setup

### 1. Clone or Open the Project
Ensure you are inside the project directory:
```bash
git clone https://github.com/rizkiarafi/weather-cli.git
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate on Windows (CMD)
.venv\Scripts\activate.bat

# Activate on macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
1. Copy the template env file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and insert your API keys:
   - **`OPENWEATHERMAP_API_KEY`**: Obtain a free API key from [OpenWeatherMap](https://openweathermap.org/).
   - **`IPLOCATE_API_KEY`**: Obtain an API key from [iplocate.io](https://iplocate.io/).

---

## Usage

Run the program from your terminal:
```bash
python weather_app.py
```

### Example Output

```text
fetch_ip_geo_api: Used cache if exists when the IP is the same with previous IP
fetch_weather_api: Used cache if exists and its age is less than 3600 seconds
                 date        weather  celc_temprature  humidity
0 2026-05-23 19:00:00  moderate rain            30.18     30.18
1 2026-05-24 19:00:00  moderate rain            28.43     28.43
2 2026-05-25 19:00:00     light rain            28.91     28.91
3 2026-05-26 19:00:00     light rain            28.35     28.35
4 2026-05-27 19:00:00     light rain            28.34     28.34
```

---

## How It Works Under the Hood

1. **IP Detection (`get_ip6`)**: Uses socket resolution to find the current host's IPv6 address.
2. **Geo-Location Lookup (`fetch_ip_geo_api`)**: Calls `iplocate.io` using the detected IP. It saves the response to `cache-data/ip-geo-cache.json` and `cache-data/ip-cache.json`.
3. **Weather Forecast Call (`fetch_weather_api`)**: Uses the retrieved latitude and longitude to call the OpenWeatherMap Forecast API.
4. **Caching Rules**:
   - The weather forecast is updated only if the local cached version is older than 1 hour or if a different user IP is detected.
   - Saves cached weather to `cache-data/weather-cache.json`.
5. **Data Downsampling**: The 5-day weather data from OpenWeatherMap comes with 40 timestamps (every 3 hours). The script downsamples this list to 5 items spaced equally across the range to show a neat 5-day outlook.
