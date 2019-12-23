# URL Shortner

## Introduction

Short URL refers to shortening a long url so users can use that short url instead of the original long url on websites, chats, e-mails, post, tweets etc.

In this application, a user can provide a long url which is shortened. The short url when used is redirected to the original url.

## The Application

### SQLiteBackend

The SQLiteBackend is responsible for creating the columns in the table and making a connection to the database.

### Database

The database contains an ID, Original url and Short url column which stores the respective urls.

### Short URL

The short url is created with Base62 which includes 0 - 9 digits, a - z lowercase and A - Z uppercase characters. 

In order to get the index characters from the Base, the mod is calculated by a number (original url's id) and base lenght (62). As the short url has to remains unique, a while loop is used to get the next index in the Base by taking the mod of the quotient and base length. The quotient is then calculated again to bring it to zero and the index are concatenated to form the short url. 

### Functions and Routes

1. Main()

The route in the main function allows users to submit a long url for shortening. Once the user submits the url, the page changes to the get short url function.

![Main page](https://github.com/StephenDsouza90/url-shortner/blob/shortner/screenshots/main.png)

2. Get_short_url()

In the get_short_url function, first the original long url is stored in the database, then the id (the number) of that original url is used to generate the short url via the Base62 system. Once the short url is generated, it is updated in the db.

![Short url](https://github.com/StephenDsouza90/url-shortner/blob/shortner/screenshots/short_url.png)

3. Redirect_url()

When the user uses the redirect (short_url) route, the redirect function redirects the short url to the original url. If the short url does not exist then it will return a 404 (not found).

4. Page_not_found()

If the short url does not exist or not created then a 404 page will return.

## How to run locally

```

>> python url_shortner.py

Connecting to sqlite:///short_url.db
Serving on http://StephenDsouza:8080

```