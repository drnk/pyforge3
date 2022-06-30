FROM python:3.10.5-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install nc
RUN apt-get update && apt-get install -y netcat

# create user
RUN useradd --create-home --shell /bin/bash app

# change work dir to user home directory
WORKDIR /home/app

#RUN python -m venv .venv
#RUN . /home/app/.venv/bin/activate

# upgrade pip and install the dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /home/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy the application
COPY . /home/app/
RUN chown app:app -R /home/app
RUN chmod +x /home/app/entrypoint.sh

# install app to user environment
RUN pip install --editable .

# change the user to different from root
USER app

ENTRYPOINT ["/home/app/entrypoint.sh"]