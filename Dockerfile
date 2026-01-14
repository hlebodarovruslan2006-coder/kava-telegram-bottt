FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY kava_bot.py .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "kava_bot.py"]
