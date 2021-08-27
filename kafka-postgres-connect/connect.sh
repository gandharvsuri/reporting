#!/bin/bash
curl -X POST -H "Accept:application/json" -H "Content-Type: application/json" --data @postgresSource.json http://localhost:8083/connectors

#Check Connection 
# curl -X GET -H "Accept:application/json" localhost:8083/connectors/anonprofile-connector