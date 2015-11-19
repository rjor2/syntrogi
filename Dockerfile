# Just Trying to get free testing from DockerHUB. Was tring to get a full user test but was finding it difficult to run
# docker or vagrant on docker itself. see privileged more in docker...

FROM django

# Rjango Rest Framework
RUN pip install djangorestframework
RUN pip install markdown
RUN pip install django-filter

# Git
RUN apt-get update
RUN apt-get install -y git-core
RUN pip install gitpython

ENV PYTHONUNBUFFERED 1

# Add code
RUN mkdir /code
ADD . /code
WORKDIR /code/webapp

# Run Tests
RUN python manage.py test

CMD "bash"
