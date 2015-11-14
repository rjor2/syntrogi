# syntrogi REST API Demo

## Installation
- Clone this git repo.
- Edit the Vagrant file. Put whatever ip you want to run on.
- Run vagrant

This might take a while. It will download everything that is necessary and automatically start the DB / django app and Server.

To Test the API you can use:

## POST
Will create the instance in the DB and download the git repo to the repos folder

```
curl -X POST --data '{"url":"*{url_of_git_repo}"}*' http://*{ip_set_in_Vagrantfile}*:8000/repos/
```

eg

```
curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi"}' http://192.168.33.21:8000/repos/

curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi", "branch":"dev"}' http://192.168.33.21:8000/repos/

curl -X POST --data '{"url":"https://github.com/rjor2/syntrogi", "branch":"dev", "revision":"4b2f362d61f2ea0d8ef1717189943195b19f29a5"}' http://192.168.33.21:8000/repos/
```

## GET
To get a list of all repos use:

```
curl -X GET http://*{ip_set_in_Vagrantfile}*:8000/repos/
```

To get date on a specific repo use:

```
curl -X GET http://*{ip_set_in_Vagrantfile}*:8000/repos/{repo_id}
```

eg

```
curl -X GET http://192.168.33.21:8000/repos/

curl -X GET http://192.168.33.21:8000/repos/58454e97-6afe-4dfd-972d-ae565f5bde82/
```

## DELETE
To delete a repo use:

```
curl -X DELETE http://*{ip_set_in_Vagrantfile}*:8000/repos/{repo_id}

curl -X DELETE http://192.168.33.21:8000/repos/58454e97-6afe-4dfd-972d-ae565f5bde82/
```

Better explanation to follow. Should be able to autogen API instructions.