# AI Logging Service
An application that exposes apis to write and retrieve log data from a manual test question session into a csv file

## Deploying the application

### Deploying locally

To run the application on your local machine, follow the steps [here](./LOCAL_DEPLOY.md):

### Deploying onto Code Engine

To deploy the application in IBM Code Engine, follow the steps [here](./CODE_ENGINE_DEPLOY.md)

### Deploying onto an OpenShift cluster

You can deploy this application onto a provisioned [Red Hat OpenShift](https://cloud.ibm.com/docs/openshift?topic=openshift-getting-started) cluster. Follow the steps [here](./OPENSHIFT_DEPLOY.md)

## Creating a custom extension for watsonx Assistant

See steps [here](./WXA.md) to connect this up to **IBM watsonx Assistant**.

## API descriptions

**POST /log/{filename}**

Write to a log file named `filename` within the `/tmp/log_service_files` subdirectory. If the file does not exist, it will be created. If it does exist, the data will be appended to the file.  The data will be saved in `csv` format to the file, so add the `.csv` extension to the filename.

**Request body**:
```
{
  "query": "User Query",
  "response": "LLM Response,
  "rating": "5 - Excellent",
  "comments": "Any additional comments on the generated response"
}
```
**GET /log/{filename}**

Get the contents of `filename`

**Response body**:
```
query,llm_response,rating,comments
User Query,LLM Response,5 - Excellent,Any additional comments on the generated response
```

**GET /logs**

Get a list of all log files contained in the `/tmp/log_service_files` directory

**Response body**:
```
[ 
  <full file path>, 
  <full file path>, 
  <full file path>, 
  <full file path>
  ...
]
```

**POST /clear_log/{filename}**

Move `filename` into a subdirectory named with datetime stamp. This saves off the log file so it isn't appended to or overwritten

**POST /clear_logs**

Move all files located in the `/tmp/log_service_files` directory into a subdirectory named with datetime stamp. This saves off logs so they aren't appended to or overwritten

**DELETE /log/{filename}**

Delete the file `filename` within the `/tmp/log_service_files` directory

**DELETE /logs**

Delete all logs located in the `/tmp/log_service_files` directory

## Example commands: 
Add logging data to logfile: 
```
curl -X 'POST' \
  'https://logging-service.1m7e1ln410px.ca-tor.codeengine.appdomain.cloud/log/test_log.csv' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "User Query",
  "llm_response": "LLM Response",
  "rating": "2",
  "comments": "Any comments"
}'
```
Retrieve the contents of a log file:
```
curl -X 'GET' \
  'https://logging-service.1m7e1ln410px.ca-tor.codeengine.appdomain.cloud/log/test_log.csv' \
  -H 'accept: application/json'
```
Clear a specific log file (move it into a dated subdirectory)
```
curl -X 'POST' \
  'https://logging-service.1m7e1ln410px.ca-tor.codeengine.appdomain.cloud/clear_log/test_log.csv' \
  -H 'accept: application/json'
```
Delete a specific log file:
```
curl -X 'DELETE' \
  'https://logging-service.1m7e1ln410px.ca-tor.codeengine.appdomain.cloud/log/test_log.csv' \
  -H 'accept: application/json'
```
Get a list of all log files:
```
curl -X 'GET' \
  'https://logging-service.1m7e1ln410px.ca-tor.codeengine.appdomain.cloud/logs' \
  -H 'accept: application/json'
```
Clear all log files (move them into a dated subdirectory)
```
curl -X 'POST' \
  'https://logging-service.1m7e1ln410px.ca-tor.codeengine.appdomain.cloud/clear_logs/test_log.csv' \
  -H 'accept: application/json' \
  -d ''
```
Delete all log files:
```
curl -X 'DELETE' \
  'https://logging-service.1m7e1ln410px.ca-tor.codeengine.appdomain.cloud/logs' \
  -H 'accept: application/json'
```


