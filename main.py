from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import base64
from io import BytesIO
from PIL import Image
import easyocr
import numpy as np

app = FastAPI()

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EasyOCR reader (English only to keep it light)
reader = easyocr.Reader(['en'], gpu=False)

@app.get("/")
async def root():
    return {"status": "ok", "message": "EasyOCR API is running!"}

@app.post("/upload")
async def upload_image(request: Request):
    try:
        data = await request.json()
        image_data = data.get("image")
        if not image_data:
            return {"error": "No image provided."}

        # Decode base64 to image
        image_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(image_bytes))

        # Run OCR
        result = reader.readtext(np.array(img), detail=0)
        text = "\n".join(result)

        return {"text": text}

    except Exception as e:
        return {"error": str(e)}
