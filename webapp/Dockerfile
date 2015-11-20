FROM django

# Rjango Rest Framework
RUN pip install djangorestframework
RUN pip install markdown
RUN pip install django-filter

# UWSGI
RUN pip install uwsgi

# Git
RUN apt-get update
RUN apt-get install -y git-core
RUN pip install gitpython

# SUPERVISOR
RUN apt-get install -y supervisor
RUN ln -s /code/supervisor-app.conf /etc/supervisor/conf.d/

# Nginx
RUN apt-get install -y nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# symlink from the default config directory to your config file
RUN ln -s /code/app_nginx.conf /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default

ENV PYTHONUNBUFFERED 1

# Add code
RUN mkdir /code
RUN mkdir /repos
ADD . /code
WORKDIR /code

# Logs for Django
RUN mkdir /var/log/django
RUN touch /var/log/django/debug.log

RUN python manage.py test

CMD bash