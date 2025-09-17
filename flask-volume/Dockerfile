FROM python:alpine

WORKDIR /app

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY app/ .

RUN mkdir -p /data && chmod 755 /data

CMD ["python", "app.py"]