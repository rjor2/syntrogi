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

RUN vagrant up

RUN curl -X GET http://192.168.33.21:8000/repos/
RUN curl -X POST --data '{"url":"https://github.com/rjor2/melosycn"}' http://192.168.33.21:8000/repos/
RUN curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi", "branch":"dev"}' http://192.168.33.21:8000/repos/
RUN curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi", "branch":"dev", "revision":"4b2f362d61f2ea0d8ef1717189943195b19f29a5"}' http://192.168.33.21:8000/repos/
RUN curl -X GET http://192.168.33.21:8000/repos/

CMD echo "User Test Finished"
