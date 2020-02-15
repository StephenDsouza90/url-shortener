# URL Shortner

## Introduction

The term short url refers to creating a link which redirects to a long url when used. Users can use the short url instead of the original long url on websites, chats, e-mails, post, tweets etc. The purpose of a short url is that it is easy to remember, looks clean and uses less space.

In this application, a short url is created by inputting a long url. The short url when used is redirected to the original url.

## Classes

This app can work with any SQL backend (such as sqlite, postgres, mysql). If you were to use a postgres database, this is how to use the app.

### SQLBackend 

A PostgreSQL "Postgres" database server is an Object-Relational Database Management System (ORDBMS) that can store data in a secure way while using the best practices. Records can be retrived from the same computer or another computer across a network.
 
The SQLBackend class is responsible for creating the engine, managing the connection to the database and handling the session. The bootstrap method in particular, is responsible for establishing a connection to the DB and creating the columns in the table.

### URL

The class URL inherits the Base object which is a collection of Table objects and their associated schema constructs. 

This class has the table name and contains an ID, Original url and Short url column which stores the respective urls.

## Database

To create a database in postgres via the postgres image from docker hub, the following command is used.

```
>> docker run --rm -it -p 5432:5432 --name postgres -e POSTGRES_USER=user_name -e POSTGRES_PASSWORD=user_password postgres
```

To run and interact with the database, the following command is used.

```
>> psql -h localhost -d <database name> -U <user_name> -W
```

## The Application

### Generating Short URL

The short url is generated with a Base62 encoder which includes 0 - 9 digits, a - z lowercase and A - Z uppercase characters. The function takes an integer and returns a unique code which is used as a short url.

The unique code is generated by getting the index (digit or character) from the Base until the divider gets the quotient to zero. By using the original url's id as the integer, this ensures that the short url's code remains unique when the index are concatenated.

### Functions and Routes

1. Main()

The route in the main function allows users to submit a long url for shortening. Once the user submits the url, the page changes to the get short url function.

![Main page](https://github.com/StephenDsouza90/url-shortner/blob/shortner/screenshots/main.png)

2. Get_short_url()

In the get_short_url function, first the original long url is stored in the database, then the id (the number) of that url is used in generating the short url via the Base62 system. Once the short url is generated, it is updated in the db.

![Short url](https://github.com/StephenDsouza90/url-shortner/blob/shortner/screenshots/short_url.png)

3. Page_not_found()

If the short url does not exist or not created then a 404 page will return.

## How to run locally

```
>> DB_URL="postgres+psycopg2://<user_name>:<user_password>@localhost:5432/<database_name>" python url_shortner.py

Connecting to PostgreSQL..
Serving on http://0.0.0.0:8080
```

## Docker

### Running in Docker

Build the image:
```
>> docker build -t urlshortener .
```

Run the container hosting the url shortener app:
```
>> docker run --rm -it -p 8080:8080 --name urlshortener -e DB_URL="postgres+psycopg2://<user_name>:<user_password>@172.17.0.1:5432/<database name>" urlshortener

Connecting to PostgreSQL..
Serving on http://0.0.0.0:8080
```
