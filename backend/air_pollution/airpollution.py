import os
from elasticsearch import Elasticsearch, helpers
import logging
from flask import request
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Elasticsearch configuration
es_host = os.getenv('ELASTICSEARCH_HOST', 'https://elasticsearch-master.elastic.svc.cluster.local:9200')
es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
es_pass = os.getenv('ELASTICSEARCH_PASS', 'elastic')
es = Elasticsearch(
    es_host,
    verify_certs=False,
    basic_auth=(es_user, es_pass),
    timeout=100
)

environmental_index_name = "environmental_data_lga"

def get_environmental_data(name):
    if name is None:
        # Query all LGAs
        query = {"query": {"match_all": {}}}
    else:
        # Query specific LGA by name
        query = {"query": {"match": {"lga_code": name}}}

    # Execute query to retrieve environmental data
    result = es.search(index=environmental_index_name, body=query)

    # Extracting data from the hits
    data = [hit['_source'] for hit in result['hits']['hits']]
    return data

# Main function that handles incoming requests
def main():
    try:
        name = request.headers.get('X-Fission-Params-Name', None)
    except KeyError:
        name = None

    data = get_environmental_data(name)
    return json.dumps(data, indent=4)