import logging
import os
import json
from elasticsearch import Elasticsearch
from datetime import datetime

# Set up logging 1
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Elasticsearch configuration
es_host = os.getenv('ES_URL', 'https://elasticsearch-master.elastic.svc.cluster.local:9200')
es_user = os.getenv('ES_USERNAME', 'elastic')
es_pass = os.getenv('ES_PASSWORD', 'elastic')

logging.debug(f"Using Elasticsearch host: {es_host}")
logging.debug(f"Using Elasticsearch user: {es_user}")

try:
    es = Elasticsearch(
        es_host,
        verify_certs=False,
        basic_auth=(es_user, es_pass),
        timeout=100
    )
    logging.debug(f"Successfully connected to Elasticsearch at {es_host}")
except Exception as e:
    logging.error(f"Error connecting to Elasticsearch: {e}")
    raise

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

    logging.debug(f"Query: {json.dumps(query)}")

    response = es.search(index="environmental_data_lga", body=query, size=1000)
    logging.debug(f"Response: {response}")

    result = {}
    for hit in response['hits']['hits']:
        source = hit['_source']
        lga_code = source['lga_code']
        site_health_advices = source['siteHealthAdvices']

        filtered_advices = [advice for advice in site_health_advices if
                            advice['since'] <= input_time <= advice['until']]

        if lga_code not in result:
            result[lga_code] = []

        for advice in filtered_advices:
            result[lga_code].append(advice)

    logging.debug(f"Result: {result}")
    return result

def main():
    request_body = os.environ.get('HTTP_BODY')
    logging.debug(f"HTTP_BODY: {request_body}")

    if request_body:
        request = json.loads(request_body)
        input_time = request.get('time')
        logging.debug(f"Received time: {input_time}")

        if not input_time:
            logging.error("Missing 'time' parameter")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'time' parameter"})
            }

        try:
            datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            logging.error("Invalid 'time' format. Use 'YYYY-MM-DDTHH:MM:SSZ'")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid 'time' format. Use 'YYYY-MM-DDTHH:MM:SSZ'"})
            }

        data = get_data_by_time(input_time)
        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }
    else:
        logging.error("No HTTP_BODY found.")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No HTTP_BODY found"})
        }
