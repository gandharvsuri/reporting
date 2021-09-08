#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import hashlib
from elasticsearch import Elasticsearch
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import count, avg, to_json, explode
from pyspark.sql import Row

import pprint
import os  
import datetime 

def getDate(date):
    return datetime.datetime.strptime(date,"%Y-%m-%d")

def getAgeGroup(birthyear, currentyear):
    age = int(currentyear) - birthyear

    if(age < 5):
        return "Child"
    elif(age < 18):
        return "Minor"
    elif(age < 60):
        return "Adult"
    else:
        return "Senior Citizen"


pp = pprint.PrettyPrinter(indent=2)


def sendRecord(rdd):
        
    list_elements = rdd.collect()
    print("got list elements")    
    for element in list_elements:
        #convert string to python dictionary
        print("record:")
        record = json.loads(element)
        pp.pprint(record)
    
def getjson(record):
    record = json.loads(record)
    ret = dict()

    profile = json.loads(record['after']['profiledata'])
    ret['gender'] = profile['new']['gender']
    ret['loc_H1'] = profile['new']['location'][0]
    ret['loc_H2'] = profile['new']['location'][1]
    reg_date = getDate(profile["Date"])
    ret['Reg_Month'] = reg_date.month
    ret['Reg_Year'] = reg_date.year
    ret['Age_group'] = getAgeGroup(profile['new']['yearOfBirth'], reg_date.year)
    ret['Languages'] = profile['new']['preferredLanguages']
    return json.dumps(ret)

def posttoES(row, index):
    row = json.loads(row)
    count = row["Count"]
    row.pop("Count")
    # row.pop("loc_H1")
    # row.pop("loc_H2")
    # row.pop("Languages")

    jsonid = hashlib.sha224(json.dumps(row).encode('ascii', 'ignore')).hexdigest()

    if es.exists(index=index, id=jsonid):
        q = {
        "script": {
            "source": "ctx._source.Count+={}".format(count),
            "lang": "painless"
            }
        }
        es.update(index=index, id = jsonid, body=q)
        

    else:
        row["Count"] = count
        es.index(index=index, id=jsonid, body=row)

def RDDfromKafkaStream(rdd):
      # Put RDD into a Dataframe
  df0 = spark.read.json(rdd)
  df0.registerTempTable( "temp_table" )
  df0 = spark.sql( """
    SELECT
      *
    FROM
      temp_table
  """ )

  if df0.count():
    df = df0.drop('Languages')
    df = df.groupBy("gender","loc_H1", "loc_H2","Reg_Month","Reg_Year","Age_group").agg(count("*").alias("Count"))

    df = df.toJSON()
    for row in df.collect():
            posttoES(row, "anonprofile")
  
 
    df0 = df0.withColumn("Languages", explode(df0.Languages))
    df0 = df0.groupBy("gender","loc_H1", "loc_H2","Reg_Month","Reg_Year","Age_group","Languages").agg(count("*").alias("Count"))
    df0.show()
    df0 = df0.toJSON()
    for row in df0.collect():
        posttoES(row, "anonprofile_language")
  

sc = SparkContext(appName="KafkaStreamFromAnonProfile")
sc.setLogLevel("WARN")
spark = SparkSession(sc)
es = Elasticsearch('elasticsearch:9200')

if __name__ == "__main__":
    
   
    if es.indices.exists('anonprofile'):
       es.indices.delete('anonprofile')

    
    if es.indices.exists('anonprofile_language'):
       es.indices.delete('anonprofile_language')
    
    es.indices.create('anonprofile')
    es.indices.create('anonprofile_language')

    ssc = StreamingContext(sc, 10)
    brokers, topic = sys.argv[1:]
    print(brokers)
    print(topic)
    kStream = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers,
                       'group.id':'ozy-group', 
                       'fetch.message.max.bytes':'15728640',
                       'auto.offset.reset':'largest'})
    lines = kStream.map(lambda x: x[1])
    lines.count().map(lambda x:'profiles in this batch: %d' % x).pprint()
    
    lines = lines.map(lambda x: getjson(x))
    # lines.foreachRDD(sendRecord)
    lines.foreachRDD(RDDfromKafkaStream)

    print("records mapped")
    # lines.foreachRDD(lambda r: toES(r))     
    #dbRecord.pprint()
    print("before start")
    ssc.start()
    print("end -----------------")
    ssc.awaitTermination() 
  