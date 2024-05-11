from elasticsearch import Elasticsearch, helpers
import geopandas as gpd
import json

es=Elasticsearch('https://127.0.0.1:9200/',
                 verify_certs=False,
                 timeout=30,
                 basic_auth=('elastic','elastic'))



index_name = 'boundary'

index_body={
    "settings":{
        "index":{
            "number_of_shards":3,
            "number_of_replicas":1
        }
    },
    "mappings": {
        "properties": {
            "LGA_NAME": {"type": "text"},
            "geometry": {"type": "text"}
            
        }
    }
}

es.indices.create(index=index_name, body=index_body)
