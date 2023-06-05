#setting base image
FROM python:3.10-slim

#for logging
ENV PYTHONUNBUFFERED 1

#for not creating .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

#specifying our working directory
WORKDIR /app/id_converter

#copying requirements.txt file to the working directory


COPY requirements.txt /app/id_converter/

RUN apt-get update \
  && apt-get -y install tesseract-ocr libtesseract-dev
RUN pip install -r requirements.txt
# Build psycopg2-binary from source -- add required dependencies

#copying the content of the backend application into our Docker container.
COPY . /app/id_converter/

#the starting command for our container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
