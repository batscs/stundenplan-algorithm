FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/src/resources/logs

COPY ./src ./src

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

ENTRYPOINT ["python", "-u", "src/python/main.py"]

CMD ["--help"]