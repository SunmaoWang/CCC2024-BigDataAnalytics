import requests
import os
import json
from elasticsearch import Elasticsearch, helpers
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

file_path = os.path.join(script_dir, 'matched_sites_with_lgas.json')
print(f"JSON file path: {file_path}")

with open(file_path, 'r') as file:
    site_data = json.load(file)

es_host = os.getenv('ELASTICSEARCH_HOST', 'https://elasticsearch-master.elastic.svc.cluster.local:9200/')
es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
es_pass = os.getenv('ELASTICSEARCH_PASS', 'elastic')

# Elasticsearch configuration
es = Elasticsearch(
    es_host,
    verify_certs=False,
    basic_auth=(es_user, es_pass)
)

# Print environment variables
logging.info(f"Using Elasticsearch host: {es_host}")
logging.info(f"Using Elasticsearch user: {es_user}")

# Index settings
index_name = "environmental_data_lga"
index_settings = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "siteName": {"type": "text"},
            "lga_code": {"type": "keyword"},  # Add ABSLGACODE as lga_code
            "geometry": {"type": "geo_point"},
            "parameters": {
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

# Check if index exists and create if not
try:
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_settings)
        logging.info("Index created successfully.")
    else:
        logging.info("Index already exists.")
except Exception as e:
    logging.error(f"An error occurred while creating index: {e}")

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
    for record in data['records']:
        site_name = record['siteName']
        record['lga_code'] = site_data[site_name]['ABSLGACODE'] if site_name in site_data else 'Unknown'

        latitude, longitude = record['geometry']['coordinates']
        record['geometry']['coordinates'] = [longitude, latitude]

        if 'parameters' in record:
            for param in record['parameters']:
                for reading in param['timeSeriesReadings']:
                    for r in reading['readings']:
                        if 'averageValue' not in r:
                            logging.warning(f"'averageValue' missing in reading: {r}")
                            continue
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

def main():
    air_quality_data = fetch_air_quality_data()
    if air_quality_data:
        index_data_to_es(air_quality_data)
    else:
        logging.info("No data received to index.")

if __name__ == "__main__":
    main()
