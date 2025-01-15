FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/src/resources/logs
RUN mkdir -p /app/src/resources/config
RUN mkdir -p /app/src/resources/output
RUN mkdir -p /app/src/resources/input

COPY ./src ./src

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

ENTRYPOINT ["python", "-u", "src/python/server.py"]

CMD ["--help"]