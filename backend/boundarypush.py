from elasticsearch import Elasticsearch, helpers
import geopandas as gpd
import json
from shapely import wkt

es=Elasticsearch('https://127.0.0.1:9200/',
                 verify_certs=False,
                 timeout=30,
                 basic_auth=('elastic','elastic'))

gdf = gpd.read_file('/home/chanwang1/CCC2024-BigDataAnalytics/data/cleaned/useful.geojson')

index_name = 'boundary'

for i in range(0,79):
    actions = {

         "LGA_NAME": gdf.loc[i]['LGA_NAME'],
        "geometry": str(gdf.loc[i]['geometry'])
            
            }

    es.index(index=index_name,id=i, body=actions)

