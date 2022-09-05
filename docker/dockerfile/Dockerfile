FROM alpine:latest
WORKDIR /webapp
RUN apk add --update python3 postgresql-dev gcc python3-dev musl-dev py-pip
COPY main.py .
COPY templates/ templates/
RUN pip install fastapi  python-multipart jinja2 psycopg2 uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]