FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src ./src

ENTRYPOINT ["python", "-u", "src/python/main.py"]

CMD ["--help"]