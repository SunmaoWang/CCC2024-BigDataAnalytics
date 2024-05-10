from elasticsearch import Elasticsearch

es = Elasticsearch('https://127.0.0.1:9200/',
                   verify_certs=False,
                   basic_auth=('elastic', 'elastic'),
                    timeout=30
)

index_name = 'chronic_diseases'

index_body = {
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "Local Government Area Code": {"type": "integer"},
            "Local Government Area Name": {"type": "text"},
            "Chronic Obstructive Pulmonary Disease RRMSE": {"type": "double"},
            "Persons with Mental and Behavioural Problems Rate per 100": {"type": "double"},
            "Asthma RRMSE": {"type": "double"},
            "Males with Mental and Behavioural Problems Rate per 100": {"type": "double"},
            "Chronic Obstructive Pulmonary Disease Count": {"type": "double"},
            "Hypertension Count": {"type": "double"},
            "Hypertension RRMSE": {"type": "double"},
            "Respiratory System Diseases Count": {"type": "double"},
            "Males with Mental and Behavioural Problems Count": {"type": "double"},
            "Females with Mental and Behavioural Problems Count": {"type": "double"},
            "Diabetes Count": {"type": "double"},
            "Circulatory System Diseases Count": {"type": "double"},
            "Musculoskeletal System Diseases Count": {"type": "double"},
            "High Cholesterol Count": {"type": "double"},
            "Arthritis Count": {"type": "double"},
            "Chronic Obstructive Pulmonary Disease Rate per 100": {"type": "double"},
            "High Cholesterol Rate per 100": {"type": "double"},
            "Asthma Rate per 100": {"type": "double"},
            "Diabetes Rate per 100": {"type": "double"},
            "Circulatory System Diseases Rate per 100": {"type": "double"},
            "Musculoskeletal System Diseases Rate per 100": {"type": "double"},
            "Arthritis Rate per 100": {"type": "double"},
            "Hypertension Rate per 100": {"type": "double"},
            "Respiratory System Diseases Rate per 100": {"type": "double"},
            "Males with Mental and Behavioural Problems RRMSE": {"type": "double"},
            "Females with Mental and Behavioural Problems RRMSE": {"type": "double"},
            "Persons with Mental and Behavioural Problems RRMSE": {"type": "double"},
            "Diabetes RRMSE": {"type": "double"},
            "Circulatory System Diseases RRMSE": {"type": "double"},
            "Musculoskeletal System Diseases RRMSE": {"type": "double"},
            "High Cholesterol RRMSE": {"type": "double"},
            "Arthritis RRMSE": {"type": "double"},
            "Respiratory System Diseases RRMSE": {"type": "double"}
        }
    }
}

es.indices.create(index=index_name, body=index_body)