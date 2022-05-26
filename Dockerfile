FROM library/python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -U pip && pip3 install -r requirements.txt

ADD . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]