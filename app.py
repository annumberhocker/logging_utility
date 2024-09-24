from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import os, sys
import uvicorn
import datetime

app = FastAPI()

# Define a file to store the CSV
csv_file = '/tmp/test_results.csv'

# Define the Pydantic model for incoming JSON structure
class DataModel(BaseModel):
    query: str
    llm_response: str
    rating: str
    comments: str



@app.post("/log-to-csv/")
async def log_to_csv(data: DataModel):
    try:

        # Create CSV if not exists
        if not os.path.exists(csv_file):
            print("Creating file")
            # Create the initial CSV with headers
            pd.DataFrame(columns=['query', 'llm_response', 'rating', 'comments']).to_csv(csv_file, index=False)

        # Load existing CSV data
        df = pd.read_csv(csv_file)

        print(data)
        
        # Convert the incoming JSON (Pydantic model) to a DataFrame
        new_data = pd.DataFrame([data.dict()])
        
        # Append the new data to the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)
        
        # Save the updated DataFrame back to the CSV
        df.to_csv(csv_file, index=False)

        return {"message": "Data appended to CSV successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

# Route to download the current history
@app.get("/logs")
async def logs():

    try:
        return FileResponse("/tmp/test_results.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
    
# Route to delete the csv. (For testing maybe we can just rename the file so that we don't lose the gathered data.)
@app.delete("/logs")
async def delete_logs():
    
    try:
        os.rename("/tmp/test_results.csv", "/tmp/"+str(datetime.datetime.now()).split('.')[0]+"_test_results.csv")
        return {"statusCode": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
    
# Run the application
if __name__ == '__main__':
    if 'uvicorn' not in sys.argv[0]:
        uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)
