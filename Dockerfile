FROM python:3.10

RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /mnt/worker
WORKDIR /mnt/worker

COPY requirements.txt ./avro/Message.avsc ./

RUN pip3 install --no-cache-dir -r requirements.txt

RUN python3 -m avro_to_python.cli Message.avsc .

COPY *.py start.sh ./

CMD ["./start.sh"]
