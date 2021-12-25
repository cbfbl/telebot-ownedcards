# syntax=docker/dockerfile:1

FROM python:3

COPY requirements.txt /

COPY first_tele_bot.py /

COPY constants.py /

COPY db_controller.py /

RUN pip install -r /requirements.txt

WORKDIR /

ENTRYPOINT [ "python", "first_tele_bot.py" ]