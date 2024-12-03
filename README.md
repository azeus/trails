# Global Trail Data Collector

This Python script collects hiking trail names from OpenStreetMap (OSM) for countries worldwide using the Overpass and Nominatim APIs. It fetches geographic boundaries for each country and extracts trail information within those boundaries.

## Features

- Collects trail names from all supported countries
- Uses OpenStreetMap data through Overpass API
- Automatically fetches country boundaries using Nominatim
- Includes footways, paths, and hiking routes
- Saves results to a JSON file for easy processing
- Implements rate limiting to respect API usage guidelines

## Prerequisites

- Python 3.x
- `requests` library

## Installation

1. Clone this repository or download the script
2. Install required dependencies:
```bash
pip install requests
```

## Configuration

Before running the script, update the User-Agent header in the `get_bounding_box()` function with your application name and contact information:

```python
headers = {
    'User-Agent': 'YourAppName (your-email@example.com)'
}
```

## Usage

Simply run the script:

```bash
python trail_collector.py
```

The script will:
1. Iterate through the predefined list of countries
2. Fetch the bounding box for each country
3. Query OpenStreetMap for trails within that country
4. Save all trail names to `all_trail_names.json`

## Output Format

The script generates a JSON file (`all_trail_names.json`) with the following structure:

```json
[
  {
    "name": "Trail Name",
    "country": "Country Name"
  },
  ...
]
```

## API Information

The script uses two APIs:

1. **Nominatim API**
   - Used for geocoding country names to bounding boxes
   - Base URL: https://nominatim.openstreetmap.org/search
   - Rate limit: 1 request per second

2. **Overpass API**
   - Used for querying OpenStreetMap data
   - Base URL: http://overpass-api.de/api/interpreter
   - Queries hiking trails, footways, and paths with names

## Limitations

- Depends on OpenStreetMap data completeness
- May miss trails that aren't properly tagged in OpenStreetMap
- Processing all countries can take significant time due to API rate limits
- Some countries might not return data due to various reasons (no data, API timeouts, etc.)

## Error Handling

The script includes basic error handling for:
- Failed API requests
- Missing country boundaries
- Network issues
- Invalid responses

Failed requests are logged but don't stop the script's execution.
