# escape=\

FROM ubuntu:latest

# install tesseract
RUN apt-get update

# install python
RUN apt-get install -y python3 python3-pip python3-venv git curl tesseract-ocr

COPY . /BotManServer
WORKDIR /BotManServer
RUN python3 -m venv ./venv
RUN ./venv/bin/python3 -m ensurepip
RUN . venv/bin/activate && pip install -r requirements.txt
# install requirements

# Run
ENV LOGFILE_PATH="/BotManServer/log.db"
EXPOSE 8000
CMD . venv/bin/activate && exec python app.py
