FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /crm_cleaning
WORKDIR /crm_cleaning

RUN apk update \
    && apk add postgresql gcc python3-dev musl-dev libffi-dev

COPY Pipfile.lock /crm_cleaning
COPY Pipfile /crm_cleaning

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY source /crm_cleaning/source
COPY project_uwsgi/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY entrypoint.sh /entrypoint.sh

RUN chown -R nobody:nogroup /crm_cleaning

EXPOSE 8000

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
