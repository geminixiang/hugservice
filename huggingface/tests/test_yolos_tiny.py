from ..yolos_tiny import yolos_tiny
from models import ObjectDetectionResult


def test_yolos_tiny(snapshot):
    img_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    res = yolos_tiny(img_url)
    assert isinstance(res, ObjectDetectionResult)