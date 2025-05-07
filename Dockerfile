FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install mysql-connector-python bcrypt cryptography

CMD ["python", "login.py"]