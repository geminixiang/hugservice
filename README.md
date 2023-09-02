# Huggingface Playground

## Feature
- [x] Support model
  - [x] [yolos-tiny](https://huggingface.co/hustvl/yolos-tiny)
  - [x] [blip_image_captioning_large](https://huggingface.co/Salesforce/blip-image-captioning-large)
- [x] Dockerize: CPU & GPU

## Quick Start
```shell
poetry shell && poetry install
uvicorn main:app --reload
```

## Dev
```shell
poetry shell && poetry install
pre-commit install --install-hooks
```

## Build

```shell
sh scripts/build.sh
docker build -t hugservice:latest .
```

## Run

### CPU
```shell
docker run -p 8000:80 --rm hugging:latest
```

### GPU
```shell
docker run --gpus all -p 8000:80 --rm hugging:latest
```



## Memo

```Dockerfile
# 6.68GB
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime AS base
ENV HF_HOME="/app/.cache/"

RUN groupadd -r geminigroup && useradd -r -g geminigroup app

COPY ./requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

FROM base AS app
COPY --chown=app:geminigroup . /app/
WORKDIR /app
USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```