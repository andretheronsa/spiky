FROM python:3.7-alpine

LABEL \
    "Author"="Andre Theron" \
    "Email"="andretheronsa@gmail.com"

COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt && \
    rm requirements.txt

COPY ./spiky/ /home/spiky/
RUN mkdir /home/work
WORKDIR /home/work

ENTRYPOINT ["python", "/home/spiky/spiky.py"]