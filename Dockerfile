# escape=\

FROM ubuntu:latest

# install tesseract
RUN apt-get update
RUN apt-get install -y tesseract-ocr

# install python
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y git

COPY . /BotManServer
WORKDIR /BotManServer
RUN python3 -m venv ./venv
RUN ./venv/bin/python3 -m ensurepip
RUN . venv/bin/activate && pip install -r requirements.txt
# install requirements

# Run
CMD echo "Running BotManServer"
EXPOSE 8000
CMD . venv/bin/activate && exec python app.py
