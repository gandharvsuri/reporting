FROM spark/clusterbase:v1

# -- Layer: Apache Spark

ARG spark_version=2.4.0
ARG hadoop_version=2.7

RUN apt-get update && \
    apt-get install -y curl  && \
    apt-get install -y wget && \
    apt-get install -y zip unzip

#RUN curl https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz 
# RUN curl https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz -o spark.tgz
RUN curl https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz -o spark.tgz
#https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz 

RUN    tar -xvf spark.tgz
RUN	mv spark-2.4.0-bin-hadoop2.7 /usr/bin && \
    mkdir /usr/bin/spark-2.4.0-bin-hadoop2.7/logs
#rm spark.tgz

RUN wget https://artifacts.elastic.co/downloads/elasticsearch-hadoop/elasticsearch-hadoop-7.4.0.zip
RUN unzip elasticsearch-hadoop-7.4.0.zip
RUN mv elasticsearch-hadoop-7.4.0 /usr/bin/spark-2.4.0-bin-hadoop2.7

RUN apt-get install -y python3-pip 
RUN pip3 install elasticsearch
RUN	pip3 install jproperties
RUN	pip3 install kafka-python
RUN	pip3 install pyspark==2.4.0
RUN	pip3 install configparser
ENV SPARK_HOME /usr/bin/spark-2.4.0-bin-hadoop2.7
#ENV SPARK_HOME /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3
# -- Runtime

WORKDIR ${SPARK_HOME}
