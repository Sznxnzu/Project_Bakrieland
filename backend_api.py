# backend.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import uuid4
import os
import subprocess
from pdf2image import convert_from_path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScreenshotRequest(BaseModel):
    html_content: str  # full HTML from frontend


@app.post("/generate-screenshot")
async def generate_screenshot(req: ScreenshotRequest):
    html_content = req.html_content
    unique_id = str(uuid4())
    html_path = f"temp/{unique_id}.html"
    pdf_path = f"temp/{unique_id}.pdf"
    png_path = f"temp/{unique_id}.png"

    # Save HTML to file
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Convert HTML to PDF (requires Google Chrome)
    try:
        subprocess.run([
            "google-chrome",
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path}",
            html_path
        ], check=True)

        # Convert PDF to PNG
        images = convert_from_path(pdf_path)
        images[0].save(png_path, "PNG")

        # Simulasi: Upload ke public folder & return URL
        final_url = f"https://yourdomain.com/screenshots/{unique_id}.png"
        os.makedirs("static/screenshots", exist_ok=True)
        images[0].save(f"static/screenshots/{unique_id}.png")

        return JSONResponse({"success": True, "image_url": final_url})

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)