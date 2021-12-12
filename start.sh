#!/bin/bash

until curl --output /dev/null --silent --head --fail http://schemaregistry:8085/subjects
do
  echo "Waiting for schema registry to be available"
  sleep 5
done

## Uploading the schema to the schema registry after escaping quotes and removing new line chars from it
#SCHEMA=$(sed 's/"/\\"/g' < ./Message.avsc)
#echo "Schema to be registered: $SCHEMA"
#RESPONSE=$(curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
#           --data "{\"schema\":\"${SCHEMA//$'\n'}\"}" \
#           http://schemaregistry:8085/subjects/Message/versions)
#echo "Schema was registered with $RESPONSE"

python -u . # `-u` for unbuffered output in the container
