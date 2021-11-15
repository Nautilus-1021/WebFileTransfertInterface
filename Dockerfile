FROM python:latest

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./wfti/ ./

ENV FLASK_APP=wfti

EXPOSE 5000

VOLUME [ "/wfti/tmp" ]

CMD flask run