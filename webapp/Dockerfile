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
WORKDIR /code

RUN chmod +x /code/docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# CMD echo hello world
# CMD python -u manage.py runserver 0.0.0.0:8000