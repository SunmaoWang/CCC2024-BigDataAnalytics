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
index_name = "chronic_diseases_epa"

lga_query = {
    "_source": "Local Government Area Name",
    "query": {
        "match_all": {}
    },
    "size": 79  # Set the size to 79 to ensure all LGAs are included
}

def get_joined_data(name):
    if name is None:
        lga_result = es.search(index=index_name, body=lga_query)
        buckets = lga_result["hits"]["hits"]
        names = []
        for bucket in buckets:
            if bucket["_source"] != dict():
                names.append(bucket["_source"]["Local Government Area Name"])
    else:
        names = []
        names.append(name)

    all_data = []

    for n in names:
      query = {
        "query": {
          "has_parent": {
            "parent_type": "chronic_diseases",
            "query": {
              "bool": {
                "must": {
                  "match": {
                    "Local Government Area Name": n
                  }
                }
              }
            },
            "inner_hits": {}
          }
        },
        "size": 1,  # This specifies you want only the most recent entry per LGA
        "sort": [
          {
            "Time": {
              "order": "desc"
            }
          }
        ]
      }

      response = es.search(index=index_name, body=query)

      if response['hits']['hits']:
        # Assuming there is at least one hit, update the data with the most recent entry
        data = response['hits']['hits'][0]['inner_hits']['chronic_diseases']['hits']['hits'][0]['_source']
        data.update(response['hits']['hits'][0]['_source'])
        all_data.append(data)

    return all_data

# Main function
def main():
    try:
        name = request.headers['X-Fission-Params-Name']
    except KeyError:
        name = None

    data = get_joined_data(name)
    return json.dumps(data, indent=4)  # Using indent for better readability in the JSON output