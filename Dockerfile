FROM python:3.10-slim

WORKDIR /app

# install libspatialindex for rtree
RUN apt-get update && \
    apt-get install -y libspatialindex-dev && \
    rm -rf /var/lib/apt/lists/*

# install other requirements for func.py
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_lg

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
