# Database spike
In this spike I will try to use a database and interact with it with a python program
## Database used
[MySQL](https://dev.mysql.com/)

## Guide Followed
https://www.w3schools.com/python/python_mysql_getstarted.asp

## Deploy mysql database with docker
```
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=nome-in-codice -e MYSQL_USER=nic -e MYSQL_PASSWORD=nic -p 3306:3306 -d mysql:8
```
from [here](https://hub.docker.com/_/mysql)