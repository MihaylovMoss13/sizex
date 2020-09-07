FROM python:3.6 as build_python
COPY requirements.txt /etc/sizex/
RUN pip install -r /etc/sizex/requirements.txt
COPY . /etc/sizex/

COPY etc/telegram.conf /etc/telegram/telegram.conf
COPY etc/telegram2.conf /etc/telegram/telegram2.conf
COPY bin/wait-for.sh /usr/local/sbin/wait-for
COPY bin/run.sh /usr/local/sbin/run_application
COPY bin/celery.sh /usr/local/sbin/run_celery

EXPOSE 8000

ENV UWSGI_WORKERS 2
ENV UWSGI_PROCESS 2

CMD ["uwsgi", "--ini", "/etc/sizex/ect/uwsgi.ini"]
