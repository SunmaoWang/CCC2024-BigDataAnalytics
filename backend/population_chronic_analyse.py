from elasticsearch import Elasticsearch

es=Elasticsearch('https://127.0.0.1:9200/',
                 verify_certs=False,
                 basic_auth=('elastic','elastic'))

# 定义查询
query = {
    "query": {
        "match_all": {}
    }
}

# 执行搜索
response = es.search(index='population2021', body=query)