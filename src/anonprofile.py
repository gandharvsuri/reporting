#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import pprint

def sendRecord(rdd):
        
    list_elements = rdd.collect()
    print("got list elements")    
    for element in list_elements:
        #convert string to python dictionary
        print("record:")
        record = json.loads(element)
        print(record)
    

if __name__ == "__main__":
     sc = SparkContext(appName="KafkaStreamFromAnonProfile")
     sc.setLogLevel("WARN")
     ssc = StreamingContext(sc, 120)
     brokers, topic = sys.argv[1:]
     print(brokers)
     print(topic)
     kStream = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers,
                        'group.id':'ozy-group', 
                        'fetch.message.max.bytes':'15728640',
                        'auto.offset.reset':'largest'})
     dbRecord = kStream.map(lambda x: x[1])
     #dbRecord = kStream.map(lambda x: x[1])
     print(dbRecord)
     print("records mapped")
     #dbRecord.count().map(lambda x:'profiles in this batch: %d' % x).pprint()
     #dbRecord.pprint()
     dbRecord.foreachRDD(sendRecord)     
     #ssc.awaitTermination()
     print("before start")
     ssc.start()
     print("end -----------------")
     ssc.awaitTermination() 
    

