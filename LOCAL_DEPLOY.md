# Running locally using python environment

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
