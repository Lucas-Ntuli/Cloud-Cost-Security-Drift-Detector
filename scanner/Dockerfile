FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash scanner

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER scanner

CMD ["python", "main.py"]
