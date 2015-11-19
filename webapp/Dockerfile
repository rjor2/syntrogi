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
WORKDIR /code

RUN chmod +x /code/docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# CMD echo hello world
# CMD python -u manage.py runserver 0.0.0.0:8000