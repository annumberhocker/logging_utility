# AI Logging Utility
An application that exposes an api to write log data from a manual test question session into a csv file

## Deploying the application

### Deploying locally using python environment

To run the application on your local machine, follow the steps [here](./LOCAL_DEPLOY.md):

### Deploying locally in a container

To deploy in a container using podman: 
```
podman build -t logging-utility .
podman run --rm -p 8000:8000 logging-utility
```

### Deploying onto Code Engine
1. Log into [IBM Cloud](cloud.ibm.com)

2. Create an IBM Cloud API Key.  See [Creating and IBM Cloud API Key](https://www.ibm.com/docs/en/app-connect/container?topic=servers-creating-cloud-api-key)

3. Create an image container registry namespace

    Open the IBM Cloud Shell from the IBM Cloud Console (4th icon from the top right, looks like a console window).
    
    Run the command:
    ```
    ibmcloud cr namespace-add <cr namespace>
    ```
    
3. Navigate to **Code Engine**

    Follow this link to get to Code Engine: https://cloud.ibm.com/codeengine/projects

    Create a new project, click the blue **Create** button

4. Create secrets within the project

    Take the **Secrets and configmaps** link, 
    
    **Registry secret**
    - Select **Create**
    - Select **Registry secret**, then **Next**
    - Enter a secret name, like `build-secret`
    - For **Target registry** choose `Other`
    - For **Registry server** enter `us.icr.io`
    - For **Password** enter your IBM Cloud API Key 
    - Select **Create**

5. Create an image build
    
    From the Code Engine Project window, select **Image builds**, then go into the **Image build** tab, click build **Create** button
    
    Under the **Source** tab:
    - Name your build (something like `logging_service`)
    - Enter **Code repo URL**  as `https://github.com/annumberhocker/logging_utility`
    - Choose the branch name, i.e. `main`
    - Select **Next**

    Under the **Strategy** tab:
    - Choose name of **Dockerfile**
    - Choose timeout value (we used 15m)
    - Choose Build resources (we used XL)
    - Select **Next**

    Under **Output** tab
    - Enter `us.icr.io` for the **Registry server**
    - Set **Registry secret** to the **Registry secret** created in step 5 above
    - Set **Namespace** to the container registry namespace you created in step 3 above
    - Select **Done**

    Once the **Configuration** is set up, in the **Build runs** pane select **Create**, then **Submit build**

6. Create an Application

    Navigate to the **Applications** tab within **Code Engine** on the left side and click **Create**.

    - Provide a name for the Application, i.e. `logging_service`
    - Choose **Use an existing container image**, and enter the image name created in step 5 for **Image reference**, i.e. `us.icr.io/<cr_namespace>/logging_service:latest`
    - Change the Ephemeral storage to 2.04
    - Limit the instance scaling to 1 and 1
    - Select **Domain mappings** to **Public**.
    - Under **Optional settings**, **Image start options** change the **Listening port** to 8000
    - Finally click **Create**

### Accessing the URL on Code Engine

Wait for the build to complete. To access the URL go into the **Applications** page within the Code Engine Project, and click the **OpenURL** link next to the newly deployed application

A quick sanity check with `<url>/docs` will take you to the swagger ui. 

## API descriptions

**POST /log/{filename}**

    Write to the log file `filename` located in `/tmp/log_service_files` subdirectory. The data will be appended in `csv` format to the file if it exists, so add the .csv extension to the filename.

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
