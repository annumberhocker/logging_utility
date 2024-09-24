from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import pandas as pd
import os
import sys
import uvicorn
import datetime
import shutil

app = FastAPI()

log_directory = "/tmp/log_service_files"  # Make sure this folder exists or set an appropriate directory

# Define the Pydantic model for incoming JSON structure
class DataModel(BaseModel):
    query: str
    llm_response: str
    rating: str
    comments: str

@app.post("/log/{filename}")
async def write_log(filename: str, data: DataModel):

    # Define a file to store the CSV
    #csv_file = 'test_results.csv'

    full_logfile_path = os.path.join(log_directory, filename)
    # Create log directory and file if it doesn't exist
    if not os.path.exists(log_directory):
        print("Creating directory")
        os.makedirs(log_directory)

    if not os.path.exists(full_logfile_path):
        # Create the initial CSV with headers
        print("Creating file")
        pd.DataFrame(columns=['query', 'llm_response', 'rating', 'comments']).to_csv(full_logfile_path, index=False)

    try:
        # Load existing CSV data
        df = pd.read_csv(full_logfile_path)

        print(data)
        
        # Convert the incoming JSON (Pydantic model) to a DataFrame
        new_data = pd.DataFrame([data.dict()])
        
        # Append the new data to the existing DataFrame
        df = pd.concat([df, new_data], ignore_index=True)
        
        # Save the updated DataFrame back to the CSV
        df.to_csv(full_logfile_path, index=False)

        return {"message": "Data appended to file successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

# Create an endpoint to retrieve a log file by its filename
@app.get("/log/{filename}")
async def retrieve_log(filename: str):
    # Construct the full path to the log file
    full_logfile_path = os.path.join(log_directory, filename)
    
    # Check if the file exists
    if os.path.exists(full_logfile_path):
        return FileResponse(full_logfile_path)
    #if os.path.exists(full_logfile_path) and full_logfile_path.endswith(".csv"):
        #return FileResponse(path=full_logfile_path, media_type='text/csv', filename=filename)
    else:
        raise HTTPException(status_code=404, detail=f"File {filename} not found. Try running the GET <url>/logs api to list log files.")

# Retrieve list of file logs
@app.get("/logs")
async def retrieve_logs():
    # Ensure the directory exists
    if not os.path.exists(log_directory):
        raise HTTPException(status_code=404, detail="Directory not found")
    
    try:
        # List all files in the log_directory
        print (os.listdir(log_directory))
        
        # Filter to include only files (exclude directories)
        #files = [f for f in files if os.path.isfile(os.path.join(log_directory, f))]
        
        # Include both files and subdirectories
        filelist = []
        for root, dirs, files in os.walk(log_directory):
            # Get relative path for root (to remove leading path for simplicity)
            relative_root = os.path.relpath(root, log_directory)
            
            # Avoid printing '.' for the base directory
            if relative_root == ".":
                relative_root = ""
            
            # Add directories separately
            # for dir_name in dirs:
            #     filelist.append({
            #         "name": os.path.join(relative_root, dir_name),
            #         "type": "directory"
            #     })
            
            # Add files
            for file_name in files:
                filelist.append(os.path.join(relative_root, file_name))
                # filelist.append({
                #     "name": os.path.join(relative_root, file_name),
                #     "type": "file"
                # })
        return filelist
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while listing files: {e}")

# Endpoint to clear/rename log file 
@app.post("/clear_log/{filename}")
async def clear_log(filename: str):
    # Construct the full path to the file
    file_path = os.path.join(log_directory, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # Create new directory based on datetime stamp
            new_dir = log_directory+"/"+str(datetime.datetime.now()).split('.')[0]
            os.makedirs(new_dir)

            # Move the file into a subdirectory 
            new_filename = os.path.join(new_dir, filename)
            os.rename(file_path,new_filename)
            print (new_filename)
            return {"message": f"File '{filename}' moved successfully to {new_filename}."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error occurred while moving the file: {e}")
    else:
        raise HTTPException(status_code=404, detail="File not found")

# Endpoint to move all log files into a subdirectory based on timedate stamp
@app.post("/clear_logs")
async def clear_logs():
    
    # Create new subdirectory
    new_dir = log_directory+"/"+str(datetime.datetime.now()).split('.')[0]
    os.makedirs(new_dir)
        
    try:
        for item in os.listdir(log_directory):
            source_path = os.path.join(log_directory, item)
            
            # Only move files, skip directories
            if os.path.isfile(source_path):
                destination_path = os.path.join(new_dir, item)
                
                # Move the file to the destination directory
                shutil.move(source_path, destination_path)

        return {"message": f"Log files moved to '{new_dir}' successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while moving files: {e}")

# Endpoint to delete a file by its filename
@app.delete("/log/{filename}")
async def delete_log(filename: str):
    file_path = os.path.join(log_directory, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"message": f"File '{filename}' successfully deleted."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error occurred while deleting the file: {e}")
    else:
        raise HTTPException(status_code=404, detail="File not found")

# Endpoint to delete all log files but not subdirectories
@app.delete("/logs")
async def delete_logs():
    try:
        # Loop through all items in the directory
        # for item in os.listdir(log_directory):
        #     item_path = os.path.join(log_directory, item)
            
            # Check if it's a file (not a directory)
            # if os.path.isfile(item_path):
            #     os.remove(item_path)  # Delete the file
            #     print(f"Deleted file: {item}")
            # else:
            #    print(f"Skipped directory: {item}")

        for item in os.listdir(log_directory):
            item_path = os.path.join(log_directory, item)
            
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Recursively delete subdirectory
            elif os.path.isfile(item_path):
                os.remove(item_path)  # Delete file

        return {"message": f"All log files deleted successfully."}
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the application
if __name__ == '__main__':
    if 'uvicorn' not in sys.argv[0]:
        uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)
