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

import pprint

pp = pprint.PrettyPrinter(indent=2)


def sendRecord(rdd):
    es_record = rdd.map(getjson)
    x= es_record.collect()
    for i in x:
        pp.pprint(i)

    # es_write_conf = {
    #     "es.nodes" : "elasticsearch",
    #     "es.port" : "9200",
    #     "es.resource" : 'anonprofile/anonprofiles',
    #     "es.input.json": "yes",
    #     "es.mapping.id": "id"
    # }
    # print("*"*30)
    
    # es_record.saveAsNewAPIHadoopFile(
    #     path='-',
    #     outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",      
    #     keyClass="org.apache.hadoop.io.NullWritable",
    #     valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    #     conf=es_write_conf)
    
def getjson(record):
    record = json.loads(record)
    ret = dict()

    ret['id'] = record['after']['id']
    ret['gender'] = record['after']['profiledata']['new']['gender']
    ret['loc_H1'] = record['after']['profiledata']['new']['location'][0]
    ret['loc_H2'] = record['after']['profiledata']['new']['location'][1]
    d = dict()
    d[ret['id']] = ret
    return d

def RDDfromKafkaStream(rdd):
      # Put RDD into a Dataframe
  df = spark.read.json(rdd)
  df.registerTempTable( "temp_table" )
  df = spark.sql( """
    SELECT
      *
    FROM
      temp_table
  """ )
  df.show()

sc = SparkContext(appName="KafkaStreamFromAnonProfile")
sc.setLogLevel("WARN")
spark = SparkSession(sc)
es = Elasticsearch('elasticsearch:9200')

if es.indices.exists('anonprofile'):
    es.indices.delete('anonprofile')
    es.indices.create('anonprofile')

if __name__ == "__main__":


     
     ssc = StreamingContext(sc, 5)
     brokers, topic = sys.argv[1:]
     print(brokers)
     print(topic)
     kStream = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers,
                        'group.id':'ozy-group', 
                        'fetch.message.max.bytes':'15728640',
                        'auto.offset.reset':'largest'})
     lines = kStream.map(lambda x: x[1])
     #dbRecord = kStream.map(lambda x: x[1])
     print("records mapped")
     lines.count().map(lambda x:'profiles in this batch: %d' % x).pprint()
     lines.foreachRDD(lambda r: RDDfromKafkaStream(r))     
     #dbRecord.pprint()

     print("before start")
     ssc.start()
     print("end -----------------")
     ssc.awaitTermination() 
    

