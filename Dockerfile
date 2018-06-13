FROM python:3.6.4-jessie
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y apt-transport-https dos2unix
RUN mkdir /source
WORKDIR /source
ADD requirements.txt /source/requirements.txt
RUN pip install -r /source/requirements.txt
ADD . /source
RUN chmod +x /source/docker-entrypoint.sh
RUN dos2unix /source/docker-entrypoint.sh
RUN rm -f /source/db.sqlite3
RUN rm -f -R /source/api/migrations
EXPOSE 8000
CMD ["/source/docker-entrypoint.sh"]