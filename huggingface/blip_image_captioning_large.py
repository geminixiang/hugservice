import requests
import torch
from loguru import logger
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor


def blip_image_captioning_large(img_url: str):
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large", torch_dtype=torch.float16
    ).to("cuda")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

    logger.info(f"Downloaded image from {img_url}")
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert("RGB")

    # conditional image captioning
    text = "a photography of"
    inputs = processor(raw_image, text, return_tensors="pt").to("cuda", torch.float16)

    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)
