FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "telegram_bot.py"]