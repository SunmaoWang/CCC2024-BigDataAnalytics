import os
from elasticsearch import Elasticsearch
import logging
from flask import request
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

es_host = os.getenv('ELASTICSEARCH_HOST', 'https://elasticsearch-master.elastic.svc.cluster.local:9200')
es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
es_pass = os.getenv('ELASTICSEARCH_PASS', 'elastic')

# Elasticsearch configuration
es = Elasticsearch(
    es_host,
    verify_certs=False,
    basic_auth=(es_user, es_pass),
    timeout=100
)

# Print environment variables
logging.info(f"Using Elasticsearch host: {es_host}")
logging.info(f"Using Elasticsearch user: {es_user}")

# Index settings
index_name = "chronic_diseases"

lga_query = {
    "_source": "Local Government Area Name",
    "query": {
        "match_all": {}
    },
    "size": 79
}

# Your Flask application code

def get_joined_data(name):
    debug_messages = []  # List to store debug messages

    debug_messages.append("Inside get_joined_data function")

    if name is None:
        debug_messages.append("Name is None, querying all LGAs")
        lga_result = es.search(index=index_name, body=lga_query)
        buckets = lga_result["hits"]["hits"]
        names = []
        for bucket in buckets:
            if bucket["_source"] != dict():
                names.append(bucket["_source"]["Local Government Area Name"])
    else:
        debug_messages.append(f"Name is {name}, querying only for this LGA")
        names = [name]

    all_data = []

    for n in names:
        debug_messages.append(f"Querying data for LGA: {n}")
        query = {
            "query": {
                "has_parent": {
                    "parent_type": "chronic_diseases",
                    'query': {
                        "bool": {
                            "must": {
                                "match": {
                                    "Local Government Area Name": n
                                }
                            }
                        }

                    },
                    'inner_hits': {}
                }
            },
            "size": 1,
        }

        debug_messages.append("Executing Elasticsearch query")  # Add debug message to list
        response = es.search(index=index_name, body=query)

        if response['hits']['hits'] != list():
            debug_messages.append("Response received from Elasticsearch")  # Add debug message to list

            data = response['hits']['hits'][0]['inner_hits']['chronic_diseases']['hits']['hits'][0]['_source']
            data.update(response['hits']['hits'][0]['_source'])

            all_data.append(data)

    return all_data, debug_messages  # Return both data and debug messages

def main():
    try:
        name = request.headers.get('X-Fission-Params-Name')
    except KeyError:
        name = None

    data, debug_messages = get_joined_data(name)  # Retrieve data and debug messages

    # Include debug messages in the output result
    output = {
        "data": data,
        "debug": debug_messages  # Include the list of debug messages in the response
    }

    json_output = json.dumps(output, indent=4)

    return json_output
