import requests
import torch
from loguru import logger
from PIL import Image, ImageDraw, ImageFont
from transformers import YolosForObjectDetection, YolosImageProcessor

from models import Labels, ObjectDetectionResult

from .utils.storages import tmp_file
from config import settings


def yolos_tiny(url: str) -> ObjectDetectionResult:
    """yolos-tiny

    Args:
        url (str): image url

    Returns:
        ObjectDetectionResult: object detection result
    """
    model = YolosForObjectDetection.from_pretrained(
        "hustvl/yolos-tiny"
    ).to(settings.compute_mode)
    image_processor = YolosImageProcessor.from_pretrained(
        "hustvl/yolos-tiny", torch_dtype=torch.float16
    )

    image = Image.open(requests.get(url, stream=True).raw)
    logger.info(f"Downloaded image from {url}")
    inputs = image_processor(
        images=image,
        return_tensors="pt"
    ).to(settings.compute_mode)  # type: ignore
    outputs = model(**inputs)  # type: ignore

    target_sizes = torch.tensor([image.size[::-1]])
    results = image_processor.post_process_object_detection(
        outputs, threshold=0.9, target_sizes=target_sizes
    )[0]
    data: list[Labels] = list()

    for score, label, box in zip(
        results["scores"], results["labels"], results["boxes"]
    ):
        box = [round(i, 2) for i in box.tolist()]
        data.append(
            Labels(
                label=model.config.id2label[label.item()],
                score=round(score.item(), 3),
                box=box,
            )
        )

    draw = ImageDraw.Draw(image)
    box_color = (255, 0, 0)  # Red color for bounding boxes
    text_color = (0, 0, 255)  # White color for text
    font_path = "Montserrat-Light.ttf"  # Replace with the path to a TrueType font file
    font_size = 12
    font = ImageFont.truetype(font_path, font_size)

    # Iterate through the data and draw bounding boxes and labels
    for item in data:
        label = item.label
        score = item.score
        box = item.box

        # Draw bounding box
        draw.rectangle(box, outline=box_color, width=2)  # type: ignore

        # Prepare label text
        label_text = f"{label} ({score:.2f})"

        # Calculate text position
        # text_width, text_height = font.getsize(label_text)

        text_x = box[0]
        text_y = box[1] - 18  # Place text just above the box

        # Draw label text
        draw.text((text_x, text_y), label_text, fill=text_color, font=font)

    return ObjectDetectionResult(labels=data, image=tmp_file(image, "jpg"))
