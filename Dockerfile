FROM python:latest

COPY app/ ./app/

RUN pip install kncloudevents

RUN pip install sklearn

RUN pip install pandas

RUN pip install numpy

RUN pip install flask

EXPOSE 8080

RUN chmod 777 app/

RUN chmod 777 app/reciever.py

RUN chmod 777 app/analytics.py

RUN chmod 777 app/run.sh

ENTRYPOINT ["/bin/bash","app/run.sh"]


