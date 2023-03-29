FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
        libxml2 \
        python3-venv
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]