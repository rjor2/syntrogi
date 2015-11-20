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
RUN mkdir /repos
ADD . /code
WORKDIR /code

# Logs for Django
RUN mkdir /var/log/django
RUN touch /var/log/django/debug.log

RUN chmod +x /code/docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# CMD echo hello world
# CMD python -u manage.py runserver 0.0.0.0:8000