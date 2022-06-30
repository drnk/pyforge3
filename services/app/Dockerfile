FROM python:3.10.5-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install nc
RUN apt-get update && apt-get install -y netcat


# change work dir to user home directory
WORKDIR /usr/src/app

# create user
RUN useradd --shell /bin/bash app
RUN chown app:app -R .

#RUN python -m venv .venv
#RUN . /usr/src/app/.venv/bin/activate

# upgrade pip and install the dependencies
RUN python -m pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# install app to user environment
RUN pip install --editable .

# change the user to different from root
USER app

ENTRYPOINT ["bash"]
CMD ["./entrypoint.sh"]
