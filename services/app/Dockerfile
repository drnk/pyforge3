FROM python:3.10.5-slim-bullseye

RUN useradd --create-home --shell /bin/bash app
WORKDIR /home/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

#RUN python -m venv .venv
#RUN . /home/app/.venv/bin/activate

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /home/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/app/

RUN pip install --editable .
RUN chown app:app ./entrypoint.sh && chmod +x ./entrypoint.sh

USER app


ENTRYPOINT ["/home/app/entrypoint.sh"]