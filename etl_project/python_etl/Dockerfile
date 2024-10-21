FROM python:3

WORKDIR /python_etl

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY source/ .
COPY input/ .

ENV PYTHONPATH=/python_etl

CMD ["python", "source/etl.py"]