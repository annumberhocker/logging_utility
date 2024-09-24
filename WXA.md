# Connecting this RAG Log service to watsonx Assistant

You connect your assistant by using the api specification to add a custom extension.

### Download the api specification

Download the [logging_utility_openapi_v1.json](./logging_utility_openapi_v1.json) specification file. 

Use this specification file to create and add the extensios to your assistant.

### Build and add extension

1.  In your assistant, on the **Integrations** page, click **Build custom extension** and use the desired specification file to build a custom extension named `RAG Logging Service`. For general instructions on building any custom extension, see [Building the custom extension](https://cloud.ibm.com/docs/watson-assistant?topic=watson-assistant-build-custom-extension#building-the-custom-extension).

1.  After you build the extension, and it appears on your **Integrations** page, click **Add** to add it to your assistant. For general instructions on adding any custom extension, see [Adding an extension to your assistant](https://cloud.ibm.com/docs/watson-assistant?topic=watson-assistant-add-custom-extension).

1.  In **Servers**, under **Server Variables**, add the url (without the https) for your hosted application as `llm_route`. 

**NOTE:** 
- If you add apis and capabilities to this application, feel free to add them to the openapi specification. The application is intended to be an example of how to get started. If you add APIs after the Actions have been created, you will need to download your Actions, upload the new Open API spec and re-upload your Actions.

- If you create actions _before_ configuring the extension, you will see errors on the actions because it could not find the extension. 
