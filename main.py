from fastapi import FastAPI
from fastapi.responses import FileResponse
from loguru import logger

from huggingface import blip_image_captioning_large, yolo
from models import ObjectDetectionResult

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    logger.info("Model loaded")


@app.get(
    "/yolos-tiny",
    name="Detect objects in an image from a URL",
    tags=["HuggingFace"],
    response_model=ObjectDetectionResult,
)
def detect(url: str) -> ObjectDetectionResult:
    """
    Detect objects in an image from a URL
    """
    return yolo(url)


@app.get(
    "/blip_image_captioning_large",
    name="Detect objects in an image from a URL",
    tags=["HuggingFace"],
    response_model=str,
)
def img2txt(url: str) -> str:
    return blip_image_captioning_large(url)


@app.get("/img/{file_name}", name="Get modified image", tags=["general"])
def get_image(file_name: str):
    return FileResponse(f"outputs/{file_name}", media_type="image/jpeg")
