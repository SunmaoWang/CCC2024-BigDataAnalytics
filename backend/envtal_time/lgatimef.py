import os
from elasticsearch import Elasticsearch, helpers
import logging
from flask import request
import json
from datetime import datetime
## Search related information from environmental_data_lga index via time
## Enter time. Ex.curl -H "X-Fission-Params-Name: 2024-05-15T18:00:00Z"
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

def get_environmental_data(time):
    query = {"query": {"match_all": {}}}
    # Execute query to retrieve environmental data
    result = es.search(index=environmental_index_name, body=query)

    # Extracting data from the hits
    data = [hit['_source'] for hit in result['hits']['hits']]

    filtered_data = filter_data_by_time(data, time)
    return filtered_data


def filter_data_by_time(data, time_str):
    filtered_data = []
    time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
    for item in data:
        site_health_advices = item.get("siteHealthAdvices", [])
        filtered_health_advices = []
        for advice in site_health_advices:
            since = datetime.strptime(advice.get("since"), "%Y-%m-%dT%H:%M:%SZ")
            until = datetime.strptime(advice.get("until"), "%Y-%m-%dT%H:%M:%SZ")
            if since <= time <= until:
                filtered_health_advices.append(advice)
        if filtered_health_advices:
            filtered_item = {
                "lga_code": item.get("lga_code"),
                "siteHealthAdvices": filtered_health_advices
            }
            filtered_data.append(filtered_item)
    return filtered_data

# Main function that handles incoming requests
def main():
    try:
        time = request.headers.get('X-Fission-Params-Name', None)
    except KeyError:
        time = None

    data = get_environmental_data(time)
    return json.dumps(data, indent=4)  # Formatting for better readability
