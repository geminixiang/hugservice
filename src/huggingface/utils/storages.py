import uuid


def tmp_file(instance, type: str):
    # Save or display the modified image
    unique_image_name = f"{uuid.uuid4()}.{type}"
    instance.save(f"outputs/{unique_image_name}")

    return f"http://localhost:8000/img/{unique_image_name}"
