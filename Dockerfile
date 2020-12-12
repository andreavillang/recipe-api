FROM python:3.9-alpine
# MAINTAINER is just a name to take note whos coding

# This line of code is just to avoid any complications when running python apps on docker
ENV PYTHONUNBUFFERED 1
# ./requirements.txt refers to our current directory. Itll copy that into docker's own 
COPY ./requirements.txt /requirements.txt
# we need to run this in order for psycopg2 to have its dependencies. We do it here becuase its after having our requirements.txt in the docker container.
RUN apk add --update --no-cache postgresql-client jpeg-dev
# --virtual means that we trying to make a temporary dependency. This is just to make sure that when we migrate to a server, we have a really minimal package.
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# RUN is basically a command we want to fire to docker
RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps
# ./app refers to our APP and /app refers to dockers /app that we denoted with mkdir
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Creating a directory for the images that are uploaded -p forces docker to make the directory if it doesnt exist.
RUN mkdir -p /vol/web/media
#  Creating a directory in the case I want to put in my own sort of files
RUN mkdir -p /vol/web/static

# the adduser command with "-D" tells docker that we're making a user named "user" and thisll be an account for the application only. note that its not glbal
RUN adduser -D user
# We created alot of directories. -R command means recursive. So all the subfolders are also added to the ownership command
RUN chown -R user:user /vol/
# This makes sure that the directory can only be accessed by the user and the rest can access with read rights only
RUN chmod -R 755 /vol/web
# swap to the user we created
USER user