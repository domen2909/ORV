FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt || true

CMD ["python", "naloga1.py"]
