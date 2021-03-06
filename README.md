# syntrogi REST API Demo

## Installation
- Clone this git repo.
```
git clone https://github.com/rjor2/syntrogi.git
```

- Edit the Vagrant file. Put whatever ip you want to run on. (cd to repo first)
```
# PUT YOUR DESIRED IP HERE
config.vm.network "private_network", ip: "xxx.xxx.xx.xx"
```
- Run vagrant
```
vagrant up
```

This might take a while. It will download everything that is necessary and automatically start the DB / django app and Server.

To Test the API from the command line you can use:

## POST
Will create the instance in the DB and download the git repo to the repos folder

```
curl -X POST --data '{"url":"{url_of_git_repo}"}' http://{ip_set_in_Vagrantfile}/repos/ --header "Content-Type:application/json"
```

eg

```
curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi"}' http://192.168.33.21/repos/ --header "Content-Type:application/json"

curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi", "branch":"dev"}' http://192.168.33.21/repos/ --header "Content-Type:application/json"

curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi", "branch":"dev", "revision":"4b2f362d61f2ea0d8ef1717189943195b19f29a5"}' http://192.168.33.21/repos/ --header "Content-Type:application/json"
```

## GET
To get a list of all repos use:

```
curl -X GET http://{ip_set_in_Vagrantfile}/repos/
```

To get date on a specific repo use:

```
curl -X GET http://{ip_set_in_Vagrantfile}/repos/{repo_id}
```

eg

```
curl -X GET http://192.168.33.21/repos/

curl -X GET http://192.168.33.21/repos/58454e97-6afe-4dfd-972d-ae565f5bde82/
```

## DELETE
To delete a repo use:

```
curl -X DELETE http://{ip_set_in_Vagrantfile}/repos/{repo_id}
```

eg

```
curl -X DELETE http://192.168.33.21/repos/58454e97-6afe-4dfd-972d-ae565f5bde82/
```

Better explanation to follow. Should be able to autogen API instructions.

## PUT
To update and existing repo use put
```
curl -X PUT --data '{"url":"{url_of_git_repo}", "branch":"{branch}", "revision":"{revision}"}' http://{ip_set_in_Vagrantfile}/repos/ --header "Content-Type:application/json"
```

eg

```
curl -X PUT --data '{"url":"https://github.com/rjor2/syntrogi", "branch":"master", "revision":"8bf352142817a650b379e818d6c1d00d6528de7c"}' http://192.168.33.21/repos/58454e97-6afe-4dfd-972d-ae565f5bde82/ --header "Content-Type:application/json"
```

You can also test in a browser just navigate to
```
http://{ip_set_in_Vagrantfile}/repos/
```
### Notes

#### SSH
You can ssh to the box using
```
vagrant ssh
```
or the default user:vagrant password:vagrant

#### DOCKER
After sshing to the box via vagrant of ssh or whatever you some simple docker commands

List all images
```
sudo docker images
```

List all running containers
```
sudo docker ps
```

Stop/start/remove/view-logs containers using Docker-compose (when in the /vagrant directory)
```
sudo docker-compose stop
sudo docker-compose up
sudo docker-compose rm
sudo docker-compose logs
```

"ssh" to docker
```
sudo docker exec -it {container-name} bash
```
eg
```
sudo docker exec -it my-webapp bash
```

#### TEST
Once in the docker web-container you can run the test suite by running
```
cd /code
python manage test
```

There is also an automatic build set up for this repo at dockerhub to view go to:
```
https://hub.docker.com/r/rjor2/syntrogi/builds/
```
