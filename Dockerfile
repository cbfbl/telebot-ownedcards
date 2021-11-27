# syntax=docker/dockerfile:1

FROM nickgryg/alpine-pandas

COPY requirements.txt /

COPY first_tele_bot.py /

COPY constants.py /

COPY data /

RUN pip install -r /requirements.txt

WORKDIR /

ENTRYPOINT [ "python", "first_tele_bot.py" ]