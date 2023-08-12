# Dockerfile, Image, Container

FROM python:3.11

ADD server_code.py .
ADD serverDB.py .
ADD data.db .

RUN pip install asyncio


CMD [ "python", "./server_code.py" ]