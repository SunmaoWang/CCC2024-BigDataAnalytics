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

population_index_name = "population2021"
useful_index_name = "useful"

def get_joined_data(name):
    all_data = []
    if name is None:
        # Query all LGAs, set size parameter to retrieve more or all entries
        population_query = {"query": {"match_all": {}}, "size": 100}
    else:
        # Query specific LGA by name, set size parameter to retrieve more or all entries
        population_query = {"query": {"match": {"LGA": name}}, "size": 100}

    # Execute queries to retrieve data
    population_result = es.search(index=population_index_name, body=population_query)

    # Get LGA codes and convert integer to keyword for compatibility
    lga_codes = [str(hit['_source']['LGA_code']) for hit in population_result['hits']['hits']]

    # Query useful data using ABSLGACODE matched to LGA codes from population
    useful_query = {"query": {"terms": {"ABSLGACODE": lga_codes}}, "size": 100}
    useful_result = es.search(index=useful_index_name, body=useful_query)

    # Process population and useful data
    for pop in population_result['hits']['hits']:
        pop_lga_code = str(pop['_source']['LGA_code'])
        combined = {**pop['_source']}
        useful_data = next((item['_source'] for item in useful_result['hits']['hits'] if str(item['_source']['ABSLGACODE']) == pop_lga_code), None)
        if useful_data:
            if 'geometry' in useful_data:
                useful_data['useful_geometry'] = useful_data.pop('geometry')
            combined.update(useful_data)
        all_data.append(combined)

    return all_data

# Main function that handles incoming requests
def main():
    try:
        name = request.headers.get('X-Fission-Params-Name', None)
    except KeyError:
        name = None

    data = get_joined_data(name)
    return json.dumps(data, indent=4)