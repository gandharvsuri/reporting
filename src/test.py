from datetime import datetime
from elasticsearch import Elasticsearch
import json
import hashlib
es = Elasticsearch('elasticsearch:9200')
# if es.indices.exists('test-index'):
#     es.indices.delete('test-index')
    
# es.indices.create('test-index')

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': 6,
}
count = 5

q = {
        # "query": {
        # "match": {
        #     'author' : 'x'
        # }
        # },
        "script": {
        "source": "ctx._source.timestamp+={}".format(count),
        "lang": "painless"
        # write the name of field and with which new value should be updated  
        }
}

print(type(doc))
t = doc.pop("timestamp")
doc['timestamp'] = t
jsonid = 1
# res = es.index(index="test-index", id=jsonid, body=doc)
# print(res['result'])

if es.exists(index="test-index", id=jsonid):
    res = es.update(index="test-index", id = jsonid, body=q)


res = es.get(index="test-index", id=1)
print(res['_source'])
es.indices.refresh(index="test-index")
res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print(hit["_source"])