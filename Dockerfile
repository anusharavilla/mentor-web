FROM python:stretch
#FROM python:3.7.2-slim

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN /bin/bash -c "source setup.sh"

ENTRYPOINT ["gunicorn", "-b", ":8080", "app:APP"]
#ENTRYPOINT [“python”, “backend/app.py”]
