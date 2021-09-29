FROM python:3.9

RUN python3.9 -m pip install --upgrade pip

COPY requirements.txt /tmp

RUN python3.9 -m pip install -r /tmp/requirements.txt

CMD [ "/bin/bash" ]