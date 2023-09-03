from pydantic import BaseModel


class Labels(BaseModel):
    label: str
    score: float
    box: list


class ObjectDetectionResult(BaseModel):
    labels: list[Labels]
    image: str
