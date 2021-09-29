FROM python:3.8

RUN python3.8 -m pip install --upgrade pip

COPY requirements.txt /tmp

RUN python3.8 -m pip install -r /tmp/requirements.txt

CMD [ "/bin/bash" ]