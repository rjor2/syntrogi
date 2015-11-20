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
ENV SECRET_KEY 5(15ds+i2+%ik6z&!yer+ga9m=e%jcqiz_5wszg)r-z!2--b2b
ENV DB_NAME postgres
ENV DB_USER postgres
ENV DB_PASS postgres
ENV DB_SERVICE db
ENV DB_PORT 5432

# Add code
RUN mkdir /code
ADD . /code
WORKDIR /code/webapp

# Logs for Django
RUN mkdir /var/log/django
RUN touch /var/log/django/debug.log

# Run Tests
RUN python manage.py test

CMD "bash"
