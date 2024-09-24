# AI Logging Utility
An application that exposes an api to write log data from a manual test question session into a csv file

## Deploying the application

### Deploying locally

To run the application on your local machine, follow these steps:

1. Navigate to the project directory:

    ```bash
    git clone https://github.com/annumberhocker/logging_utility.git
    cd logging_utility
    ```

3. Create a Python Enviroment, Activate it, and Install Requirements:

    ```bash
    python -m venv assetEnv
    source assetEnv/bin/activate
    python -m pip install -r requirements.txt
     ```

4. Start the project:

    ```bash
    python app.py
    ```

5. URL access:

    The url, for purposes of using cURL is http://0.0.0.0:8000.

    To access Swagger go to http://0.0.0.0:8000/docs
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

A quick sanity check with `<url>/docs` will take you to the swagger ui. To try the APIs from swagger, you will need to click the **Authorize** button at the top and add the value you set for RAG-APP-API-KEY in the environment variables

## Example request
```
{
  "query": "User Query",
  "response": "LLM Response,
  "rating": "1 - Excellent",
  "comments": "Any additional comments on the generated response"
}
```
## Output

This will append the data as a line in a local csv file called `test_results.csv`


