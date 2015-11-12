# The reason for this Dockerfile is so that I can get free automated testbuilds. My interconnection is a little slow. So
# I'm off loading the vagrant up to docker's auto build which is hooked up to the git repo :D

FROM ubuntu:trusty

# Update
RUN apt-get update

# Install vagrant
RUN apt-get install -y vagrant

# Install vBox
RUN echo "deb http://download.virtualbox.org/virtualbox/debian trusty contrib" >> /etc/apt/sources.list
RUN curl -L https://www.virtualbox.org/download/oracle_vbox.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y virtualbox-5.0

# Add code
RUN mkdir /code
ADD . /code
WORKDIR /code

# CMD vagrant up
