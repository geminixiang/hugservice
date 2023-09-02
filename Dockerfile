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