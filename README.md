[![Build Status](https://travis-ci.org/AndrewMishchenko/sqltomongo.svg?branch=master)](https://travis-ci.org/AndrewMishchenko/sqltomongo)
[![Docker Build Statu](https://img.shields.io/docker/build/jrottenberg/ffmpeg.svg)](https://cloud.docker.com/app/andrewmishchenko/repository/docker/andrewmishchenko/sqltomongo/general)

### Sqltomongo:
* Sqltomongo is a CLI (command line interface) to work with MongoDB much easier. 
* Sqltomongo translates SQL (Structured Query Language) queries to MongoDB queries.
* Sqltomongo uses the builtin MongoDB module.

### Installation
Download from github repository:
```sh 
https://github.com/AndrewMishchenko/sqltomongo 
```
or (if you have already installed git) just do:
```sh
git clone https://github.com/AndrewMishchenko/sqltomongo.git
```
Go to the downloaded repository 
```sh
cd sqltomongo/
```
and type: 
```sh
sudo pip3 install .
```
After installation type:
```sh
sqltomongo
```
in the shell and you will see something like:
```sh
Sqltomongo shell version v0.1 >
```
### If everything is ok you can already work with sqltomongo shell.

### The sqltomongo shell
> It is assumed that you have installed and started MongoDB.

When you run sqltomongo without any arguments, the sqltomongo shell will attempt to connect to the MongoDB instance running on the *localhost* interface on port *27017*. To specify a different database, host or port number, as well as other options you must type:
```sh 
sqltomongo database_name host port
```
For example, if you want to run “test” database with the standart localhost (127.0.0.1) and standart port (27017) you must type:
```sh 
sqltomongo test
```
or if you want to run “test” database with 127.0.0.1 host and 27017 port you must type:
```sh 
sqltomongo test 127.0.0.1 27017
```
To  specify the database – use *‘use’* method in the *sqltomongo* shell. For example:
```sh 
use test
```
and it will switch to test database.
If you want to display the database you are using, just type: 
```sh 
db
```
in the sqltomongo shell and you will see the name of the using database.

To *authenticate* in the database you are using just type:
```sh 
auth (user, passwd)
```
in the sqltomongo shell and you will see 1 if ok and 0 if authentication failed. 

### Sqltomongo works only with SELECT statement!

*The structure of the SQL should be as follows:*
>[SELECT <Projections>*] 
[FROM <Target>]
[WHERE <Condition> *]
[ORDER BY <Fields>  [ASC | DESC]]
[SKIP <SkipRecords>]
[LIMIT <MaxRecords>]

Projections form - \*, field, field.subfield, field.\*. Where "field.\*" is the mongo db aggregations.

Support condition for operations  “=, <>,>,>=, <, <=”. 
Also include the standard logical operations like *AND, OR* to combine Conditions.

*Does not support the subqueries.*

### Examples:

| Sqltomongo | MongoDB |
| --------- | ------ |
| select \* from restaurants | db.restaurants.find({}) |
| select \* from restaurants where restaurant_id > '40361521' | db.restaurants.find({'restaurant_id': {'$gt': '40361521'}}) |
| select restaurant_id, address.coord.* from restaurants where restaurant_id > '40356731' order by restaurant_id desc limit 5 | db.restaurants.aggregate({'$match': {'restaurant_id': {'$gt': '40356731'}}}, {'$project': {'restaurant_id': 1, 'address.coord': 1}}, {'$unwind': '$address.coord'}, {'$sort': {'restaurant_id': -1}}, {'$limit': 5}) |


### Sqltomongo is licensed under the BSD license.
