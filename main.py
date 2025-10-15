from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64, io
from PIL import Image
import pytesseract

app = FastAPI()

# allow your laptop to call it from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/upload")
async def upload(req: Request):
    """
    Receives JSON: {"image": "<base64 image>"}
    Returns: {"text": "<ocr result>"}
    """
    try:
        data = await req.json()
        if "image" not in data:
            return JSONResponse({"error": "Missing 'image' field"}, status_code=400)

        # decode base64 → image
        img_bytes = base64.b64decode(data["image"])
        img = Image.open(io.BytesIO(img_bytes))

        # OCR
        text = pytesseract.image_to_string(img, lang="eng")

        return {"text": text.strip()}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
