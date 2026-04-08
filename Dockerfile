FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install pandas pydantic openai flask

CMD ["python", "app.py"]