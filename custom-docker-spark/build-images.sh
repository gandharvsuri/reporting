#!/bin/sh
export SPARK_VERSION="2.4.0"
export HADOOP_VERSION="2.7"
export JUPYTERLAB_VERSION="2.1.5"
docker build -f clusterBase.Dockerfile -t spark/clusterbase:v1 .
docker build --build-arg spark_version="${SPARK_VERSION}" --build-arg hadoop_version="${HADOOP_VERSION}" -f SparkBase.Dockerfile -t spark/sparkbase:v1 .
docker build -f SparkMaster.Dockerfile -t spark/sparkmaster:v1 .
docker build -f SparkWorker.Dockerfile -t spark/sparkworker:v1 .
docker build -f JupiterLab.Dockerfile -t spark/jupiterlab:v1 .
