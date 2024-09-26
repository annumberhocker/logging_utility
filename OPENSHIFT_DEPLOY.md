# How to Deploy this Application on OpenShift

To deploy this project on OpenShift, follow these steps:

1. Log in to your OpenShift cluster:

    ```bash
    oc login --token=YOUR_TOKEN --server=YOUR_SERVER
    ```

1. Create a new project (optional):

    ```bash
    oc new-project ai-logging-service
    ```
1. Change into new project
    ```
    oc project ai-logging-service
    ```
1. Build the application:
    ```bash
    oc new-build --strategy docker --binary --name=ai-logging-service
    oc start-build ai-logging-service --from-dir=. --follow --wait
    oc new-app ai-logging-service --name=ai-logging-service
    ```
    or
    ```
    oc new-app python:latest~https://github.com/ibm-build-lab/ai-logging-service.git  --name=ai-logging-service --strategy=source
    ```
    To monitor the build process:
    ```
    oc logs -f bc/my-python-app
    ```
1. Expose a Secure URL for this FastAPI app:
    ```bash
    oc create route edge --service=ai-logging-service
    ```

A quick sanity check with the url created from the route: `<route>/docs` will take you to the swagger ui.
