from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
import geopandas as gpd
import shapely
import sys

pd.set_option('display.max_rows', 60)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 80)
sys.setrecursionlimit(100000)

es = Elasticsearch('https://127.0.0.1:9200/',
                   verify_certs=False,
                   basic_auth=('elastic', 'elastic'),
                   timeout=300
                  )

with open('./data/cleaned/chronic_disease.json', 'r') as file:
    chronic_data = pd.read_json(file)

with open('./data/cleaned/LGA_useful_geo/lga_for_join.json', 'r') as file:
    geo_data = gpd.read_file(file)

geo_data["geometry"] = geo_data["geometry"].apply(lambda x: shapely.geometry.mapping(x))

chronic_data['Local Government Area Name'] = chronic_data['Local Government Area Name'].apply(lambda x: ' '.join(x.split()[:-1]).lower())

chronic_data.at[51, 'Local Government Area Name'] = "merri-bek"

data = geo_data.set_index('LGA_NAME').join(chronic_data.set_index('Local Government Area Name')).reset_index()

index_name = 'chronic_diseases_epa'

actions = [
    {
        "_index": index_name,
        "_id": i,
        "_source": {
            "Local Government Area Code": row['Local Government Area Code'],
            "Local Government Area Name": str(row['LGA_NAME']),
            "Local Government Area Shape": row['geometry'],
            "Chronic Obstructive Pulmonary Disease RRMSE": row['Chronic Obstructive Pulmonary Disease RRMSE'],
            "Persons with Mental and Behavioural Problems Rate per 100": row['Persons with Mental and Behavioural Problems Rate per 100'],
            "Asthma RRMSE": row['Asthma RRMSE'],
            "Males with Mental and Behavioural Problems Rate per 100": row['Males with Mental and Behavioural Problems Rate per 100'],
            "Chronic Obstructive Pulmonary Disease Count": row['Chronic Obstructive Pulmonary Disease Count'],
            "Hypertension Count": row['Hypertension Count'],
            "Hypertension RRMSE": row['Hypertension RRMSE'],
            "Respiratory System Diseases Count": row['Respiratory System Diseases Count'],
            "Males with Mental and Behavioural Problems Count": row['Males with Mental and Behavioural Problems Count'],
            "High Cholesterol Rate per 100": row['High Cholesterol Rate per 100'],
            "Asthma Rate per 100": row['Asthma Rate per 100'],
            "Diabetes Rate per 100": row['Diabetes Rate per 100'],
            "Musculoskeletal System Diseases RRMSE": row['Musculoskeletal System Diseases RRMSE'],
            "Females with Mental and Behavioural Problems RRMSE": row['Females with Mental and Behavioural Problems RRMSE'],
            "Arthritis Count": row['Arthritis Count'],
            "Respiratory System Diseases Rate per 100": row['Respiratory System Diseases Rate per 100'],
            "Arthritis Rate per 100": row['Arthritis Rate per 100'],
            "Hypertension Rate per 100": row['Hypertension Rate per 100'],
            "Circulatory System Diseases Rate per 100": row['Circulatory System Diseases Rate per 100'],
            "Females with Mental and Behavioural Problems Count": row['Females with Mental and Behavioural Problems Count'],
            "Diabetes RRMSE": row['Diabetes RRMSE'],
            "High Cholesterol Count": row['High Cholesterol Count'],
            "Circulatory System Diseases RRMSE": row['Circulatory System Diseases RRMSE'],
            "Respiratory System Diseases RRMSE": row['Respiratory System Diseases RRMSE'],
            "Persons with Mental and Behavioural Problems RRMSE": row['Persons with Mental and Behavioural Problems RRMSE'],
            "Diabetes Count": row['Diabetes Count'],
            "Asthma Count": row['Asthma Count'],
            "Persons with Mental and Behavioural Problems Count": row['Persons with Mental and Behavioural Problems Count'],
            "Females with Mental and Behavioural Problems Rate per 100": row['Females with Mental and Behavioural Problems Rate per 100'],
            "Circulatory System Diseases Count": row['Circulatory System Diseases Count'],
            "Musculoskeletal System Diseases Rate per 100": row['Musculoskeletal System Diseases Rate per 100'],
            "Musculoskeletal System Diseases Count": row['Musculoskeletal System Diseases Count'],
            "Arthritis RRMSE": row['Arthritis RRMSE'],
            "Males with Mental and Behavioural Problems RRMSE": row['Males with Mental and Behavioural Problems RRMSE'],
            "Chronic Obstructive Pulmonary Disease Rate per 100": row['Chronic Obstructive Pulmonary Disease Rate per 100'],
            "High Cholesterol RRMSE": row['High Cholesterol RRMSE'],
            "relation_type": {
                "name": "chronic_diseases"
            }
        }
    }
    for i, row in list(data.iterrows())
]

helpers.bulk(es, actions)