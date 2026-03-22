from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse #fixing the issue of file not being downloaded.
from rembg import remove
from fastapi.middleware.cors import CORSMiddleware #fixing the issue of different port(8000-uvicorn, 5500-loalhost)
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    return {"status": "ok"}

'''
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    output = remove(image)

    buffer = io.BytesIO()
    output.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
'''
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()

    output_bytes = remove(input_bytes)  # ✅ FIX

    return StreamingResponse(
        io.BytesIO(output_bytes),
        media_type="image/png"
    )