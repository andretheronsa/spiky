ARG IMAGE_VERSION=buster
ARG IMAGE_VARIANT=-slim
FROM debian:$IMAGE_VERSION$IMAGE_VARIANT

LABEL \
    "Author"="Andre Theron" \
    "Email"="andretheronsa@gmail.com"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip

ADD requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt