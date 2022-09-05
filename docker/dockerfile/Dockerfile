FROM alpine:latest
WORKDIR /webapp
RUN apk add --update python3 postgresql-dev gcc python3-dev musl-dev py-pip
RUN pip install fastapi  python-multipart jinja2 psycopg2 uvicorn
COPY webapp_src/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]