import os
from elasticsearch import Elasticsearch, helpers
import logging
from flask import Flask, request, jsonify
from datetime import datetime
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

# Print environment variables
logging.info(f"Using Elasticsearch host: {es_host}")
logging.info(f"Using Elasticsearch user: {es_user}")


# Function to get data based on the given date and time
def get_data_by_time(input_time):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "siteHealthAdvices.since": {
                                "lte": input_time
                            }
                        }
                    },
                    {
                        "range": {
                            "siteHealthAdvices.until": {
                                "gte": input_time
                            }
                        }
                    }
                ]
            }
        }
    }

    response = es.search(index="environmental_data_lga", body=query, size=1000)

    result = {}
    for hit in response['hits']['hits']:
        source = hit['_source']
        lga_code = source['lga_code']
        site_health_advices = source['siteHealthAdvices']

        # Filter site health advices by input time
        filtered_advices = [advice for advice in site_health_advices if
                            advice['since'] <= input_time <= advice['until']]

        if lga_code not in result:
            result[lga_code] = []

        for advice in filtered_advices:
            result[lga_code].append(advice)

    return result


def main():
    request = json.loads(os.environ.get('HTTP_BODY'))
    input_time = request.get('time')

    if not input_time:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'time' parameter"})
        }

    try:
        # Ensure the input time is in the correct format
        datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid 'time' format. Use 'YYYY-MM-DDTHH:MM:SSZ'"})
        }

    data = get_data_by_time(input_time)
    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }