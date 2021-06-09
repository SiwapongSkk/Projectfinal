import cv2
import numpy as np
import pytesseract
import io


from fastapi import FastAPI, File, UploadFile, Request

from fastapi.responses import HTMLResponse
from typing import List


from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.templating import Jinja2Templates
import shutil
import ocr
import os
import uuid
import json
import base64

from pydantic import BaseModel


from typing import Optional

from fastapi import FastAPI

app = FastAPI()

a = cv2.__version__


@app.get("/")
def read_root():
    return {"Hello": "World11"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# upload single file
@app.post("/img")
async def up_img_book(file: UploadFile = File(...)):
    contents = await file.read()
    image_stream = io.BytesIO(contents)
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    label =  ocr.read_img(frame)

    return  { "File Name": file.filename, "label": label}


##---------------------
class Abc(BaseModel):
    image : str 


# upload single file
@app.post("/imgg")
async def up_img_book(file: Abc ):
    contents = base64.b64decode(file.image)
    image_stream = io.BytesIO(contents)
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    label =  ocr.read_img(frame)
    return  { "label": label}



##-----------------


#app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/0")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




@app.post("/extract_text") 
async def extract_text(request: Request):
    label = ""
    if request.method == "POST":
        form = await request.form()
        # file = form["upload_file"].file
        contents = await form["upload_file"].read()
        image_stream = io.BytesIO(contents)
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        label,cropped_img =  ocr.read_img(frame)

        #encoded_image_string = base64.b64encode(cropped_img)
        #print(encoded_image_string)
       
        #lda = label.address

        #return {"label": label}
   
    return templates.TemplateResponse("index.html", {"request": request, "label": label,"cropped_img": cropped_img})