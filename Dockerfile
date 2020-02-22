FROM python:3.7-slim

LABEL \
    "Author"="Andre Theron" \
    "Email"="andretheronsa@gmail.com"

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
