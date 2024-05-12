import os
from elasticsearch import Elasticsearch

es_host = os.getenv('ELASTICSEARCH_HOST', 'https://127.0.0.1:9200/')
es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
es_pass = os.getenv('ELASTICSEARCH_PASS', 'elastic')

es = Elasticsearch(
    es_host,
    verify_certs=False,  # Consider enabling certificate verification in production environments
    basic_auth=(es_user, es_pass)
)

# Fetch unique LGA codes
lga_query = {
    "query": {
        "match_all": {}
    },
    "aggs": {
        "unique_lga_codes": {
            "terms": {
                "field": "Local Government Area Code",
                "size": 1000
            }
        }
    }
}

# Fetch health data for diseases
health_query = {
    "size": 1000,  # Adjust based on expected document count
    "query": {
        "match_all": {}
    }
}

try:
    lga_result = es.search(index="chronic_diseases", body=lga_query)
    lga_codes = [bucket["key"] for bucket in lga_result["aggregations"]["unique_lga_codes"]["buckets"]]
    print("Unique LGA Codes:", lga_codes)

    health_result = es.search(index="environmental_data", body=health_query)
    health_data = []
    for doc in health_result['hits']['hits']:
        site_name = doc['_source'].get('siteName')
        coordinates = doc['_source'].get('geometry', {}).get('coordinates')
        if 'siteHealthAdvices' in doc['_source']:
            for advice in doc['_source']['siteHealthAdvices']:
                health_parameter = advice.get('healthParameter')
                health_advice = advice.get('healthAdvice')
                average_value = advice.get('averageValue')
                health_data.append({
                    'Site Name': site_name,
                    'Coordinates': coordinates,
                    'Health Parameter': health_parameter,
                    'Health Advice': health_advice,
                    'Average Value': average_value
                })

    print("Health Data:", health_data)

except Exception as e:
    print("Failed to fetch data from Elasticsearch:", e)
