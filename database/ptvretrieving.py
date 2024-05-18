import requests
import hmac
from hashlib import sha1
import os
from elasticsearch import Elasticsearch, helpers
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read configuration from file
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read().strip()

# Elasticsearch Configuration
es_host = config('ELASTICSEARCH_HOST')
es_user = config('ELASTICSEARCH_USER')
es_pass = config('ELASTICSEARCH_PASS')
es = Elasticsearch(
    es_host,
    verify_certs=False,
    basic_auth=(es_user, es_pass),
    timeout=30
)

# Index settings
index_name = "environmental_data"
index_settings = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
        # Fill in
    }}

# Check if index exists and create if not
try:
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_settings)
        logging.info("Index created successfully.")
    else:
        logging.info("Index already exists.")
except Exception as e:
    logging.error(f"An error occurred while creating index: {e}")


# API Signature method
def generate_api_url(request):
    devId = 2
    key = bytes(config('API_SECRET'), 'utf-8')
    request = request + ('&' if ('?' in request) else '?') + f'devid={devId}'
    raw = request.encode('utf-8')
    hashed = hmac.new(key, raw, sha1)
    signature = hashed.hexdigest()
    return f"http://timetableapi.ptv.vic.gov.au{request}&signature={signature}"

# Function to fetch data from the API
def fetch_data(api_url):
    url = generate_api_url(api_url)
    headers = {
        "Cache-Control": "no-cache",
        "User-Agent": "MyApp/1.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logging.error(f"Failed to fetch data: HTTP {response.status_code} - {response.text}")
        return None

# Index data to Elasticsearch
def index_data_to_es(data):
    actions = [{
        "_index": "api_data",
        "_source": # fill in}]
    
    try:
        helpers.bulk(es, actions)
        logging.info("Data indexed successfully.")
    except helpers.BulkIndexError as e:
        logging.error(f"Error indexing data: {e.errors}")

# Main function
def main():
    api_url = # API endpoint
    data = fetch_data(api_url)
    if data:
        index_data_to_es(data)
    else:
        logging.info("No data received to index.")

if __name__ == "__main__":
    main()
