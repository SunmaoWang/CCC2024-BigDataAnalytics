from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch('https://127.0.0.1:9200/',
                   verify_certs=False,
                   basic_auth=('elastic', 'elastic'),
                   timeout=30
                   )

with open('./data/cleaned/chronic_disease.json', 'r') as file:
    data = json.load(file)

index_name = 'chronic_diseases'

actions = [
    {
        "_index": index_name,
        "_id": key,
        "_source": {
            "Local Government Area Code": data['Local Government Area Code'].get(key),
            "Local Government Area Name": data['Local Government Area Name'].get(key),
            "Chronic Obstructive Pulmonary Disease RRMSE": data['Chronic Obstructive Pulmonary Disease RRMSE'].get(key, None),
            "Persons with Mental and Behavioural Problems Rate per 100": data['Persons with Mental and Behavioural Problems Rate per 100'].get(key, None),
            "Asthma RRMSE": data['Asthma RRMSE'].get(key, None),
            "Males with Mental and Behavioural Problems Rate per 100": data['Males with Mental and Behavioural Problems Rate per 100'].get(key, None),
            "Chronic Obstructive Pulmonary Disease Count": data['Chronic Obstructive Pulmonary Disease Count'].get(key, None),
            "Hypertension Count": data['Hypertension Count'].get(key, None),
            "Hypertension RRMSE": data['Hypertension RRMSE'].get(key, None),
            "Respiratory System Diseases Count": data['Respiratory System Diseases Count'].get(key, None),
            "Males with Mental and Behavioural Problems Count": data['Males with Mental and Behavioural Problems Count'].get(key, None),
            "High Cholesterol Rate per 100": data['High Cholesterol Rate per 100'].get(key, None),
            "Asthma Rate per 100": data['Asthma Rate per 100'].get(key, None),
            "Diabetes Rate per 100": data['Diabetes Rate per 100'].get(key, None),
            "Musculoskeletal System Diseases RRMSE": data['Musculoskeletal System Diseases RRMSE'].get(key, None),
            "Females with Mental and Behavioural Problems RRMSE": data['Females with Mental and Behavioural Problems RRMSE'].get(key, None),
            "Arthritis Count": data['Arthritis Count'].get(key, None),
            "Respiratory System Diseases Rate per 100": data['Respiratory System Diseases Rate per 100'].get(key, None),
            "Arthritis Rate per 100": data['Arthritis Rate per 100'].get(key, None),
            "Hypertension Rate per 100": data['Hypertension Rate per 100'].get(key, None),
            "Circulatory System Diseases Rate per 100": data['Circulatory System Diseases Rate per 100'].get(key, None),
            "Females with Mental and Behavioural Problems Count": data['Females with Mental and Behavioural Problems Count'].get(key, None),
            "Diabetes RRMSE": data['Diabetes RRMSE'].get(key, None),
            "High Cholesterol Count": data['High Cholesterol Count'].get(key, None),
            "Circulatory System Diseases RRMSE": data['Circulatory System Diseases RRMSE'].get(key, None),
            "Respiratory System Diseases RRMSE": data['Respiratory System Diseases RRMSE'].get(key, None),
            "Persons with Mental and Behavioural Problems RRMSE": data['Persons with Mental and Behavioural Problems RRMSE'].get(key, None),
            "Diabetes Count": data['Diabetes Count'].get(key, None),
            "Asthma Count": data['Asthma Count'].get(key, None),
            "Persons with Mental and Behavioural Problems Count": data['Persons with Mental and Behavioural Problems Count'].get(key, None),
            "Females with Mental and Behavioural Problems Rate per 100": data['Females with Mental and Behavioural Problems Rate per 100'].get(key, None),
            "Circulatory System Diseases Count": data['Circulatory System Diseases Count'].get(key, None),
            "Musculoskeletal System Diseases Rate per 100": data['Musculoskeletal System Diseases Rate per 100'].get(key, None),
            "Musculoskeletal System Diseases Count": data['Musculoskeletal System Diseases Count'].get(key, None),
            "Arthritis RRMSE": data['Arthritis RRMSE'].get(key, None),
            "Males with Mental and Behavioural Problems RRMSE": data['Males with Mental and Behavioural Problems RRMSE'].get(key, None),
            "Chronic Obstructive Pulmonary Disease Rate per 100": data['Chronic Obstructive Pulmonary Disease Rate per 100'].get(key, None),
            "High Cholesterol RRMSE": data['High Cholesterol RRMSE'].get(key, None)
        }
    }
    for key in data['Local Government Area Code'].keys()
]

helpers.bulk(es, actions)