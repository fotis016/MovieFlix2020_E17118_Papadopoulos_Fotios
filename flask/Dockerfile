FROM ubuntu:16.04
MAINTAINER fotis_papadopoulos <tottinos86@gmail.com>
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y bcrypt
RUN pip3 install flask pymongo
RUN pip3 install Flask-PyMongo py-bcrypt
RUN mkdir /app
RUN mkdir -p /app/static
RUN mkdir -p /app/templates
COPY web_service.py /app/web_service.py
ADD static /app/static
ADD templates /app/templates
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "web_service.py" ]
