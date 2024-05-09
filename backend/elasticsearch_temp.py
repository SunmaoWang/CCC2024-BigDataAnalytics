from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dotenv import load_dotenv
import json
import os

client = Elasticsearch()

# testing
# print(client.info())

# pre-defined variable
INDEX_NAME = "data_sudo"

# Create insertion index
def create_index():
    index_body = {
        "settings": {
            "index": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text"},
                "course": {"type": "text"},
                "mark": {"type": "short"}
            }
        }

    }
    response = client.indices.create(index=INDEX_NAME, body=index_body)
    return response

# data insertion as whole
def data_insertion():
    student_data = [
        {
            "_index": INDEX_NAME,
            "_id": "0000",
            "_source": {
                "name": "John Smith",
                "course": "Cloud Computing",
                "mark": 80
            }
        },
        {
           "_index": INDEX_NAME,
            "_id": "1111",
            "_source": {
                "name": "Jane Doe",
                "course": "Cloud Computing",
                "mark": 90
            }
        }
    ]
    response = bulk(client, student_data)
    return response

# Querying
