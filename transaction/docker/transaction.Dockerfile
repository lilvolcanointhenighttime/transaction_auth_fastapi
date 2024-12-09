from python:3.12.4-slim

LABEL name="fastapi_transaction"

WORKDIR .
RUN mkdir /src

COPY ./transaction/config/req.txt /src/transaction/req.txt
RUN python -m pip install -r ./src/transaction/req.txt

COPY ./transaction /src/transaction/