ARG IMAGE_VERSION=buster
ARG IMAGE_VARIANT=-slim
FROM debian:$IMAGE_VERSION$IMAGE_VARIANT

LABEL \
    "Author"="Andre Theron" \
    "Email"="andretheronsa@gmail.com"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3=3.7.3-1 \
    python3-pip=18.1-5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
