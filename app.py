from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os, sys
import uvicorn


app = FastAPI()

# Define a file to store the CSV
csv_file = '/tmp/test_results.csv'

# Define the Pydantic model for incoming JSON structure
class DataModel(BaseModel):
    query: str
    llm_response: str
    rating: str
    comments: str

# Create CSV if not exists
if not os.path.exists(csv_file):
    # Create the initial CSV with headers
    pd.DataFrame(columns=['query', 'llm_response', 'rating', 'comments']).to_csv(csv_file, index=False)

@app.post("/log-to-csv/")
async def log_to_csv(data: DataModel):
    try:
        # Load existing CSV data
        df = pd.read_csv(csv_file)
        
        # Convert the incoming JSON (Pydantic model) to a DataFrame
        new_data = pd.DataFrame([data.dict()])
        
        # Append the new data to the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)
        
        # Save the updated DataFrame back to the CSV
        df.to_csv(csv_file, index=False)

        return {"message": "Data appended to CSV successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

# Run the application
if __name__ == '__main__':
    if 'uvicorn' not in sys.argv[0]:
        uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)
