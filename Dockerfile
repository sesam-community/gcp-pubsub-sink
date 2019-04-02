FROM python:3.6-slim

MAINTAINER Simen Jorgensen "simen.jorgensen@sesam.io"

COPY ./service /service
WORKDIR /service

RUN pip install -r requirements.txt

EXPOSE 5000/tcp

ENTRYPOINT ["python3"]
CMD ["pubsubservice.py"]