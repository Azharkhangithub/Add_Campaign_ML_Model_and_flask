FROM python:3.8

MAINTAINER Azhar

WORKDIR /app

COPY './requirements.txt' .

# RUN apt-get install libgtk2.0-dev pkg-config -yqq 

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["app.py"]