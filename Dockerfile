# FROM command tells docker what "image" is to be used.
FROM python:3.9-alpine
# MAINTAINER is just a name to take note whos coding

# This line of code is just to avoid any complications when running python apps on docker
ENV PYTHONUNBUFFERED 1
# ./requirements.txt refers to our current directory. Itll copy that into docker's own 
COPY ./requirements.txt /requirements.txt
# we need to run this in order for psycopg2 to have its dependencies. We do it here becuase its after having our requirements.txt in the docker container.
RUN apk add --update --no-cache postgresql-client
# --virtual means that we trying to make a temporary dependency. This is just to make sure that when we migrate to a server, we have a really minimal package.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
# RUN is basically a command we want to fire to docker
RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps
# ./app refers to our APP and /app refers to dockers /app that we denoted with mkdir
RUN mkdir /app
WORKDIR /app
COPY ./app /app
# the adduser command with "-D" tells docker that we're making a user named "user" and thisll be an account for the application only. note that its not glbal
RUN adduser -D user
# swap to the user we created
USER user