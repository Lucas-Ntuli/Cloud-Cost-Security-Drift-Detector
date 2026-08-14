FROM python:3.12-slim-bookworm 

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash scanner

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==26.1.2 \
    && pip install --no-cache-dir  -r requirements.txt

COPY . .  

USER scanner

CMD ["python", "main.py"]