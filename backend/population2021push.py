from elasticsearch import Elasticsearch, helpers
import json

es=Elasticsearch('https://127.0.0.1:9200/',
                 verify_certs=False,
                 basic_auth=('elastic','elastic'))

with open('./data/cleaned/population2021.json', 'r') as file:
    data = json.load(file)

index_name = 'population2021'

actions = [
    {
        "_index": index_name,
        "_id": key,
        "_source": {
            "LGA_code": key,
            "LGA": data['LGA'][str(key)],
            "2021Persons0-4": data['2021Persons0-4'].get(str(key), 0),
            "2021Persons5-9": data['2021Persons5-9'].get(str(key), 0),
            "2021Persons10-14": data['2021Persons10-14'].get(str(key), 0),
            "2021Persons15-19": data['2021Persons15-19'].get(str(key), 0),
            "2021Persons20-24": data['2021Persons20-24'].get(str(key), 0),
            "2021Persons25-29": data['2021Persons25-29'].get(str(key), 0),
            "2021Persons30-34": data['2021Persons30-34'].get(str(key), 0),
            "2021Persons35-39": data['2021Persons35-39'].get(str(key), 0),
            "2021Persons40-44": data['2021Persons40-44'].get(str(key), 0),
            "2021Persons45-49": data['2021Persons45-49'].get(str(key), 0),
            "2021Persons50-54": data['2021Persons50-54'].get(str(key), 0),
            "2021Persons55-59": data['2021Persons55-59'].get(str(key), 0),
            "2021Persons60-64": data['2021Persons60-64'].get(str(key), 0),
            "2021Persons65-69": data['2021Persons65-69'].get(str(key), 0),
            "2021Persons70-74": data['2021Persons70-74'].get(str(key), 0),
            "2021Persons75-79": data['2021Persons75-79'].get(str(key), 0),
            "2021Persons80-84": data['2021Persons80-84'].get(str(key), 0),
            "2021Persons85+": data['2021Persons85+'].get(str(key), 0),
            "2021Persons_total": data['2021Persons_total'].get(str(key), 0)
        }
    }
    for key in data['LGA  code'].keys()
]


helpers.bulk(es, actions)