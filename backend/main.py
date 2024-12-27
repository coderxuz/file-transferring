from fastapi import FastAPI, File, UploadFile, HTTPException, status, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from typing import Dict
import uuid
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

os.makedirs(name="uploads", exist_ok=True)
active_connections:Dict[str, WebSocket] = {}

def delete_file_after_delay(file_location:str, delay:int):
    time.sleep(delay)
    if os.path.exists(file_location):
        os.remove(file_location)
        print(f"Deleted file: {file_location}")


@app.post("/")
async def upload(background_task:BackgroundTasks,file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb+") as file_obj:
        file_obj.write(file.file.read())
    
    background_task.add_task(delete_file_after_delay, file_location, 600)

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

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    user_id = str(uuid.uuid4())
    print(user_id)
    active_connections[user_id] = websocket
    print(active_connections)
    try:
        while True:
            url = await websocket.receive_text()
            for value in active_connections.values():
                await value.send_text(url)
    except WebSocketDisconnect:
        active_connections.pop(user_id)
        print(active_connections)

