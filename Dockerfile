FROM python:3.13-slim

WORKDIR /workspace

COPY . /workspace

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

ENTRYPOINT ["python", "-m", "harnessctl.cli"]
