#!/bin/bash
curl -X POST http://localhost:8083/connectors -H "Accept:application/json" -H "Content-Type: application/json" --data @/home/gandharv/MOSIP/reporting/kafka-postgres-connect/$1 

# curl -X POST -H "Accept:application/json" -H "Content-Type: application/json" --data @/home/gandharv/MOSIP/reporting/kafka-postgres-connect/localhostConnector.json http://localhost:8083/connectors

#Check Connection 
# curl -X GET -H "Accept:application/json" localhost:8083/connectors/anonprofile-connector