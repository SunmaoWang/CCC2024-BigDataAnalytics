from elasticsearch import Elasticsearch, helpers
import json

es=Elasticsearch('https://127.0.0.1:9200/',
                 verify_certs=False,
                 basic_auth=('elastic','elastic'))

index_name = 'population2021'

index_body={
    "settings":{
        "index":{
            "number_of_shards":3,
            "number_of_replicas":1
        }
    },
    "mappings": {
        "properties": {
            "LGA_code": {"type": "integer"},
            "LGA": {"type": "text"},
            "2021Persons0-4": {"type": "integer"},
            "2021Persons5-9": {"type": "integer"},
            "2021Persons10-14": {"type": "integer"},
            "2021Persons15-19": {"type": "integer"},
            "2021Persons20-24": {"type": "integer"},
            "2021Persons25-29": {"type": "integer"},
            "2021Persons30-34": {"type": "integer"},
            "2021Persons35-39": {"type": "integer"},
            "2021Persons40-44": {"type": "integer"},
            "2021Persons45-49": {"type": "integer"},
            "2021Persons50-54": {"type": "integer"},
            "2021Persons55-59": {"type": "integer"},
            "2021Persons60-64": {"type": "integer"},
            "2021Persons65-69": {"type": "integer"},
            "2021Persons70-74": {"type": "integer"},
            "2021Persons75-79": {"type": "integer"},
            "2021Persons80-84": {"type": "integer"},
            "2021Persons85+": {"type": "integer"},
            "2021Persons_total": {"type": "integer"}
        }
    }
}

es.indices.create(index=index_name, body=index_body)


    
