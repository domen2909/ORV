FROM python:3.9-slim

WORKDIR /app

# Kopiraj requirements.txt
COPY requirements.txt .

# Namesti odvisnosti
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj preostanek kode
COPY . .

# Definiraj privzeti ukaz za zagon
CMD ["python", "naloga1.py"]
