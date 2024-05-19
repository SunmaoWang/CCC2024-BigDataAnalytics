import json
from flask import request
from elasticsearch import Elasticsearch

def main():
    lga_name = request.headers.get('X-Fission-Params-Lga-Name')

    es = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    if lga_name:
        query = {
            "query": {
                "match": {
                    "Local Government Area Name": lga_name
                }
            }
        }
    else:
        query = {"match_all": {}}

    diseases = [
        "Arthritis Count", "Asthma Count",
        "Chronic Obstructive Pulmonary Disease Count",
        "Circulatory System Diseases Count",
        "Diabetes Count",
        "Females with Mental and Behavioural Problems Count",
        "High Cholesterol Count",
        "Hypertension Count",
        "Males with Mental and Behavioural Problems Count",
        "Musculoskeletal System Diseases Count",
        "Persons with Mental and Behavioural Problems Count",
        "Respiratory System Diseases Count"
    ]

    response = es.search(index='chronic_diseases', body={
        "size": 0,
        "query": query["query"],
        "aggs": {
            "disease_counts": {
                "multi_terms": {
                    "terms": [{ "field": disease } for disease in diseases]
                }
            }
        }
    })

    result = {disease: 0 for disease in diseases}
    for bucket in response['aggregations']['disease_counts']['buckets']:
        for idx, disease in enumerate(diseases):
            result[disease] += bucket['key'][idx]

    return json.dumps(result)