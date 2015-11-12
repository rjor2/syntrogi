FROM django

RUN pip install djangorestframework
RUN pip install markdown
RUN pip install django-filter

# Add code
RUN mkdir /code
ADD . /code
WORKDIR /code

CMD python manage.py runserver 0.0.0.0:8000