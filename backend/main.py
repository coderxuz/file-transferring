from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

os.makedirs(name="uploads", exist_ok=True)


@app.post("/")
async def upload(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb+") as file_obj:
        file_obj.write(file.file.read())

    return {"location": file_location}


@app.get("/")
async def get_file(file_location: str):

    if not os.path.exists(file_location):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="is not found"
        )
    if not os.path.isfile(file_location):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="is not found"
        )
    
    return FileResponse(file_location)