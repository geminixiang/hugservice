# Huggingface Playground

- [Huggingface Playground](#huggingface-playground)
  - [Feature](#feature)
  - [Quick Start](#quick-start)
  - [Dev](#dev)
  - [Build](#build)
  - [Run](#run)
  - [Notes](#notes)
    - [方案一：僅使用 `pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime`](#方案一僅使用-pytorchpytorch201-cuda117-cudnn8-runtime)
    - [方案二：使用 `python:3.10.13-slim-bullseye` + `nvidia/cuda:12.2.0-base-ubuntu20.04` + 自行安裝 python](#方案二使用-python31013-slim-bullseye--nvidiacuda1220-base-ubuntu2004--自行安裝-python)
    - [結論](#結論)

## Feature
- [x] Support model
  - [x] [yolos-tiny](https://huggingface.co/hustvl/yolos-tiny)
  - [x] [blip_image_captioning_large](https://huggingface.co/Salesforce/blip-image-captioning-large)
- [x] Dockerize: CPU & GPU

## Quick Start
```shell
poetry shell && poetry install --with dev
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
docker build -t hugservice:gpu -f Dockerfile-gpu .
docker build -t hugservice:latest .
```

## Run

```shell
docker run --gpus all -p 8000:80 --rm hugservice:latest
```

---

## Notes

測試使用不同的方式打包，Docker image size 是否能夠下降一些

基本環境條件
- [x] CUDA
- [x] python 3.10
- [x] Pytorch

### 方案一：僅使用 `pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime`

```Dockerfile
# 6.68GB
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime AS base
COPY ./requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

FROM base AS app
...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

### 方案二：使用 `python:3.10.13-slim-bullseye` + `nvidia/cuda:12.2.0-base-ubuntu20.04` + 自行安裝 python

```Dockerfile
# 4.98GB
FROM python:3.10.13-slim-bullseye AS base

FROM base AS builder
COPY ./requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

FROM nvidia/cuda:12.2.0-base-ubuntu20.04 AS app
# 因為該image無python環境
# 額外參考 https://github.com/docker-library/python/blob/master/3.10/slim-bullseye/Dockerfile
...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

### 結論

最終採用方案二，並且將 cuda + python 環境額外使用 Dockerfile-gpu 來提前建置該環境，最後容量為 4.98GB
