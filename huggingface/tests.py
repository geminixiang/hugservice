from .blip_image_captioning_large import blip_image_captioning_large
from .yolos_tiny import yolos_tiny
from models import ObjectDetectionResult


def test_blip_image_captioning_large():
    img_url = "https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg"
    text = blip_image_captioning_large(img_url)
    assert text.startswith("a photography of")


def test_yolos_tiny():
    img_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    res = yolos_tiny(img_url)
    assert isinstance(res, ObjectDetectionResult)