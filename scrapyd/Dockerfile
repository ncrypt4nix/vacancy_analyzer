FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1
EXPOSE 6800

RUN groupadd scrapy && \
    useradd -m -g scrapy scrapy

RUN mkdir /srv/project \
          /srv/logs && \
    chown -R scrapy:scrapy /srv/*
WORKDIR /srv/project
VOLUME /srv/logs

COPY requirements.txt /srv/project/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm /srv/project/requirements.txt
USER scrapy

COPY --chown=scrapy:scrapy . /srv/project/
CMD scrapyd
