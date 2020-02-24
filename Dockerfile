FROM python:3.7-slim

LABEL \
    "Author"="Andre Theron" \
    "Email"="andretheronsa@gmail.com"

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt && \
    rm requirements.txt

COPY ./spiky/ /home/spiky/
RUN mkdir /home/work
WORKDIR /home/work

ENTRYPOINT ["python", "/home/spiky/spiky.py"]