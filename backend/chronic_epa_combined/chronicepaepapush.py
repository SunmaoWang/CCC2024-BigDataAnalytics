import requests
import logging
from elasticsearch import Elasticsearch
import os

index_name = "chronic_diseases_epa"

es_host = os.getenv('ELASTICSEARCH_HOST', 'https://elasticsearch-master.elastic.svc.cluster.local:9200')
es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
es_pass = os.getenv('ELASTICSEARCH_PASS', 'elastic')

# Elasticsearch configuration
es = Elasticsearch(
    es_host,
    verify_certs=False,
    basic_auth=(es_user, es_pass),
    timeout=30
)

# Function to fetch data from the API
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

geoshape_query = {
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_shape": {
          "Local Government Area Shape": {
            "shape": {
              "type": "point",
            },
            "relation": "contains"
          }
        }
      }
    }
  }
}

def index_data_to_es(data):
    for record in data['records']:
        latitude, longitude = record['geometry']['coordinates']
        geoshape_query["query"]["bool"]["filter"]["geo_shape"]["Local Government Area Shape"]["shape"]["coordinates"] = [longitude, latitude]
        response = es.search(index=index_name, body=geoshape_query)
        parent = response["hits"]["hits"][0]['_id']

        if 'parameters' in record:
            for param in record['parameters']:
                for reading in param['timeSeriesReadings']:
                    for r in reading['readings']:
                        if 'averageValue' not in r:
                            logging.warning(f"'averageValue' missing in reading: {r}")
                            continue  # Skip this reading
                        r['averageValue'] = float(r['averageValue'])

                        if 'confidence' in r:
                            r['confidence'] = int(r['confidence'])
                        else:
                            logging.warning(f"'confidence' missing in reading: {r}")
            
            record['relation_type'] = {'name': 'epa', 'parent': parent}
            pageDict = {
                    "Site Name": record['siteName'],
                    "Parameters": record['parameters'],
                    "Time": record['siteHealthAdvices'][0]['since'],
                    "relation_type": {'name': 'epa', 'parent': parent}
            }
            es.index(index=index_name, body=pageDict, routing=parent, id=record['siteID'] + record['siteHealthAdvices'][0]['since'])

# Main function
def main():

    air_quality_data = fetch_air_quality_data()
    if air_quality_data:
        index_data_to_es(air_quality_data)
    else:
        logging.info("No data received to index.")
    return 'OK'