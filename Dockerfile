FROM python:3.11-slim

WORKDIR /project

COPY app/requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

COPY app/ ./app/
COPY data/ ./data/

WORKDIR /project/app

EXPOSE 5000
EXPOSE 8501

CMD ["python", "app.py"]