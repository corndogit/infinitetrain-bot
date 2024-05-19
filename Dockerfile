FROM python:3.10.14-bookworm as build-base

WORKDIR /build-base
RUN apt update && apt install -y build-essential cmake
RUN git clone https://github.com/aixxe/infinitetrain

WORKDIR ./infinitetrain
RUN cmake . && make


FROM python:3.10.14-slim-bookworm as runtime

RUN apt update && apt install -y ffmpeg

ENV INFINITETRAIN_PATH=/app/infinitetrain/
COPY --from=build-base /build-base/infinitetrain/infinitetrain /build-base/infinitetrain/tracks.yml $INFINITETRAIN_PATH
WORKDIR /app

COPY requirements.txt src ./
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "__main__.py"]
