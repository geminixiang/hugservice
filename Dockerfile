FROM python:3.10.13-slim-bullseye AS base

# Install dependencies
FROM base AS builder
COPY ./requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Run server
FROM hugservice:gpu AS app
ENV HF_HOME="/app/.cache/"
RUN groupadd -r geminigroup && useradd -r -g geminigroup app
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib /usr/local/lib
COPY --chown=app:geminigroup . /app/

WORKDIR /app
USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]