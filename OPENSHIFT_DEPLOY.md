# How to Deploy this Application on OpenShift

To deploy this project on OpenShift, follow these steps:

1. Log in to your OpenShift cluster:

    ```bash
    oc login --token=YOUR_TOKEN --server=YOUR_SERVER
    ```

1. Create a new project (optional):

    ```bash
    oc new-project <project-name>
    ```
1. Change into new project
    ```
    oc project <project-name>
    ```
1. Build the application:
    ```bash
    $ oc new-build --strategy docker --binary --name=rag_logging_service
    $ oc start-build rag_logging_service  --from-dir=. --follow --wait
    ```
1. Deploy the application:
    ```bash
    $ oc new-app rag_logging_service --name=rag_logging_service
    ```
1. Expose a Secure URL for this FastAPI app:
    ```bash
    $ oc create route edge --service=rag_logging_service
    ```

A quick sanity check with the url created from the route: `<route>/docs` will take you to the swagger ui.
