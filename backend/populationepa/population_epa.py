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
environmental_index_name = "environmental_data_lga"

def get_joined_data(name):
    all_data = []
    if name is None:
        # Query all LGAs
        population_query = {
            "query": {
                "match_all": {}
            }
        }
        environmental_query = {
            "query": {
                "match_all": {}
            }
        }
    else:
        # Query specific LGA by name
        population_query = {
            "query": {
                "match": {
                    "LGA": name
                }
            }
        }

    # Execute population data query to retrieve LGA code
    population_result = es.search(index=population_index_name, body=population_query)
    if not population_result['hits']['hits']:
        return []  # If no matching population record is found, return empty result

    # Get LGA codes and convert integer to keyword for compatibility
    lga_codes = [str(hit['_source']['LGA_code']) for hit in population_result['hits']['hits']]

    # Query environmental data using LGA code as keyword
    environmental_query = {
        "query": {
            "terms": {
                "lga_code": lga_codes
            }
        }
    }

    # Execute environmental data query
    environmental_result = es.search(index=environmental_index_name, body=environmental_query)

    # Combine data from both queries
    for pop in population_result['hits']['hits']:
        pop_lga_code = str(pop['_source']['LGA_code'])
        for env in environmental_result['hits']['hits']:
            if pop_lga_code == env['_source']['lga_code']:
                combined = {**pop['_source'], **env['_source']}
                all_data.append(combined)

    return all_data

# Main function that handles incoming requests
def main():
    try:
        name = request.headers.get('X-Fission-Params-Name', None)
    except KeyError:
        name = None

    data = get_joined_data(name)
    return json.dumps(data)