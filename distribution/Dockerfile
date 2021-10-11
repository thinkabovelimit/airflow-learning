FROM ubuntu:18.04

# Fix for asking tz configuration for awscli package
# https://serverfault.com/questions/683605/docker-container-time-timezone-will-not-reflect-changes
ENV TZ=Asia
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev python3-dev python3-pip curl software-properties-common unzip



RUN pip3 install -U pip  \
    && rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED 1

RUN mkdir /code /var/logs /var/logs/airflow

RUN mkdir /airflow

COPY requirements.txt /airflow

WORKDIR /airflow

RUN pip3 install -r requirements.txt

COPY ./code/ /airflow/
COPY ./configs/ /airflow/

RUN touch /airflow/__init__.py
ENV AIRFLOW_HOME=/airflow
ENV PYTHONPATH="/airflow"

RUN groupadd -g 999 thor && \
    useradd -r -u 999 -g thor thor

RUN chown -R thor:thor /var/logs

RUN chown -R thor:thor /airflow

USER thor
