FROM python:3.10.5-slim-bullseye

RUN useradd --shell /bin/bash app
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

#RUN python -m venv .venv
#RUN . /usr/src/app/.venv/bin/activate

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --editable .
RUN chown app:app -R . && chmod +x ./entrypoint.sh

USER app


ENTRYPOINT ["./entrypoint.sh"]