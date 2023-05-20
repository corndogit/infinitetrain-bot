FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip build-essential ffmpeg

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["./src/__main__.py"]
