# AI Logging Utility
An application that exposes an api to write log data from a manual test question session into a csv file

## Deploying the application

### Deploying locally

To run the application on your local machine, follow the steps [here](./LOCAL_DEPLOY.md):

### Deploying onto Code Engine

To deploy the application in IBM Code Engine, follow the steps [here](./CODE_ENGINE_DEPLOY.md)

### Deploying onto an OpenShift cluster

To deploy onto OpenShift follow the steps [here](./OPENSHIFT_DEPLOY.md)

## API descriptions

**POST /log/{filename}**

Write to the log file `filename` located in `/tmp/log_service_files` subdirectory. The data will be appended in `csv` format to the file if it exists, so add the `.csv` extension to the filename.

**Request body**:
```
{
  "query": "User Query",
  "response": "LLM Response,
  "rating": "1 - Excellent",
  "comments": "Any additional comments on the generated response"
}
```
**GET /log/{filename}**

Get the contents of `filename`

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

**DELETE /log/{filename}**

    Delete the file `filename` within the `/tmp/log_service_files` directory

**GET /logs**

    Get a list of all log files contained in the `/tmp/log_service_files` directory

**DELETE /logs**

    Delete all logs located in the `/tmp/log_service_files` directory

**POST /clear_log/{filename}**

    Move `filename` into a subdirectory named with datetime stamp. This saves off the log file so it isn't appended to or overwritten

**POST /clear_logs**

    Move all files located in the `/tmp/log_service_files` directory into a subdirectory named with datetime stamp. This saves off logs so they aren't appended to or overwritten
