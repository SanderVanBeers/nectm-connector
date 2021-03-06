FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP connector.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["flask", "run"]