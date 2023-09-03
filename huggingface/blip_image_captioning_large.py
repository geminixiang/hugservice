import requests
import torch
from loguru import logger
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
from config import settings


def blip_image_captioning_large(img_url: str) -> str:
    """blip-image-captioning-large
    https://huggingface.co/Salesforce/blip-image-captioning-large

    Args:
        img_url (str): Image URL

    Returns:
        str: Generated text
    """
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    ).to(settings.compute_mode)
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

    logger.info(f"Downloaded image from {img_url}")
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert("RGB")

    # conditional image captioning
    text = "a photography of"
    inputs = processor(raw_image, text, return_tensors="pt").to(settings.compute_mode)

    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)
