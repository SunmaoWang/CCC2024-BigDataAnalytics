import requests
import os
from elasticsearch import Elasticsearch, helpers
import logging
from pyproj import Transformer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

es_host = os.getenv('ELASTICSEARCH_HOST', 'https://127.0.0.1:9200/')
es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
es_pass = os.getenv('ELASTICSEARCH_PASS', 'elastic')

# Elasticsearch configuration
es = Elasticsearch(
    es_host,
    verify_certs=False,
    basic_auth=(es_user, es_pass)
)

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")

# Print environment variables
logging.info(f"Using Elasticsearch host: {es_host}")
logging.info(f"Using Elasticsearch user: {es_user}")

# Index settings
index_name = "chronic_diseases_epa"

index_settings = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "Site Name": {"type": "text"},
            "Parameters": {
                "type": "nested",
                "properties": {
                    "name": {"type": "text"},
                    "timeSeriesReadings": {
                        "type": "nested",
                        "properties": {
                            "averageValue": {"type": "float"},
                            "unit": {"type": "keyword"},
                            "confidence": {"type": "integer"}
                        }
                    }
                }
            }
        }
    }
}

geoshape_query = {
  "query": {
    "geo_shape": {
      "Local Governemnt Area Shape": { 
        "relation": "intersects",
        "shape": {
          "type":  "point",
        }
      }
    }
  }
}


# Function to fetch data from the API
def fetch_air_quality_data():
    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"
    headers = {
        "Cache-Control": "no-cache",
        "X-API-Key": "b8c291bd447c46d197d7fef195bd4194",
        "User-Agent": "MyApp/1.0"
    }
    response = requests.get(url, headers=headers)
    logging.debug(f"Response status code: {response.status_code}")
    logging.debug(f"Response text: {response.text}")
    if response.status_code == 200:
        data = response.json()
        logging.debug(f"Data fetched: {data}")
        return data
    else:
        logging.error(f"Failed to fetch data: HTTP {response.status_code} - {response.text}")
        return None

def index_data_to_es(data):
    actions = []
    for record in data['records'][0:2]:
        latitude, longitude = record['geometry']['coordinates']
        print(latitude, longitude)
        geoshape_query["query"]["geo_shape"]["Local Governemnt Area Shape"]["shape"]["coordinates"] = [latitude, longitude]
        response = es.search(index=index_name, body=geoshape_query)
        print(response)

        """
        if 'parameters' in record:
            for param in record['parameters']:
                for reading in param['timeSeriesReadings']:
                    for r in reading['readings']:
                        if 'averageValue' not in r:
                            logging.warning(f"'averageValue' missing in reading: {r}")
                            continue  # Skip this reading
                        r['averageValue'] = float(r['averageValue'])

                        if 'confidence' in r:
                            r['confidence'] = int(r['confidence'])
                        else:
                            logging.warning(f"'confidence' missing in reading: {r}")

            action = {
                "_index": index_name,
                "_source": record
            }
            actions.append(action)

    try:
        helpers.bulk(es, actions)
        logging.info("Data indexed successfully.")
    except helpers.BulkIndexError as e:
        logging.error(f"Error indexing data: {e.errors}")
        """

# Main function
def main():
    air_quality_data = fetch_air_quality_data()
    if air_quality_data:
        index_data_to_es(air_quality_data)
    else:
        logging.info("No data received to index.")

if __name__ == "__main__":
    main()
