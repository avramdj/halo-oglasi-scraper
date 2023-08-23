FROM selenium/standalone-chrome:114.0-20230614

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN sudo apt update -y && sudo apt upgrade -y
RUN sudo apt install python3-pip -y
RUN pip3 install -r /tmp/requirements.txt
COPY . /app
WORKDIR /app
CMD ["python3", "-m", "scraper"]