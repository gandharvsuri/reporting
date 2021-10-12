from datetime import datetime
from elasticsearch import Elasticsearch
import json

import pprint
pp = pprint.PrettyPrinter(indent=2)

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
    "doc" : doc,
    "doc_as_upsert" : True
}

print(type(doc))
# t = doc.pop("timestamp")
# doc['timestamp'] = t
jsonid = 1
doc = json.dumps(doc)
print(type(doc))

anon_prof = {
"Date": "2021-09-18",
"new": {
"biometricInfo": [
{
"attempts": 0,
"digitalId": "Sample",
"qualityScore": "Sample",
"subType": "Sample",
"type": "Sample"
}
],
"channel": [
{
"hashedchannel": "a234aa6b0d1e1233b85e1947039468033a758a261c6396c201c768fff7b63ca0",
"name": "phone"
}
],
"exceptions": [
""
],
"gender": "Female",
"location": [
"Arunachal Pradesh",
"Hayuliang"
],
"preferredLanguages": [
"tam"
],
"verified": [
"gender,dob"
],
"yearOfBirth": 1960
},
"old": {
"biometricInfo": [
{
"attempts": 0,
"digitalId": "Sample",
"qualityScore": "Sample",
"subType": "Sample 2",
"type": "Sample 2"
},
{
"attempts": 0,
"digitalId": "Sample",
"qualityScore": "Sample",
"subType": "Sample 3",
"type": "Sample 3"
}
],
"channel": [
{
"hashedchannel": "a234aa6b0d1e1233b85e1947039468033a758a261c6396c201c768fff7b63ca0",
"name": "phone"
}
],
"exceptions": [
""
],
"gender": "Female",
"location": [
"Arunachal Pradesh",
"Hayuliang"
],
"preferredLanguages": [
"tam"
],
"verified": [
"gender,dob"
],
"yearOfBirth": 1960
},
"processName": "NEW"
}

print(type(anon_prof))
anon_prof = json.dumps(anon_prof)
print(type(anon_prof))

res = es.index(index="test-index", id=jsonid, body=anon_prof)
pp.pprint(res)

# if es.exists(index="test-index", id=jsonid):
#     res = es.update(index="test-index", id = jsonid, body=q)


# res = es.get(index="test-index", id=1)
# print(res['_source'])
# es.indices.refresh(index="test-index")
# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print(type(hit["_source"]))
#     print(hit["_source"])