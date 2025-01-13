FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src ./src

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

ENTRYPOINT ["python", "-u", "src/python/server.py"]

CMD ["--help"]