FROM python:3.5-alpine
WORKDIR /usr/src/app

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=0

COPY app/app.py .
COPY app/whitelist.txt .

CMD [ "flask", "run", "--host", "0.0.0.0" ]
