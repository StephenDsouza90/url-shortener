# URL Shortner

## Introduction

Short URL refers to shortening a long url so that users can use that short url instead of the original long url on websites, chats, e-mails, post, tweets etc.

In this application, a user can provide a long url which is shortened. The short url when used is redirected to the original url.

## The Application

### SQLiteBackend

The SQLiteBackend is responsible for creating the columns in the table and making a connection to the database.

### Database

The database contains an ID, Original url and Short url column which stores the respective urls.

### Short URL

The short url is create with Base64 (digits, lowercase and uppercase characters) and creates a combination of 5 characters long.

### Functions and Routes

1. Main()

The route in the main function allows users to submit a long url for shortening. Once the user submits the url, the page changes to the add url function.

![Main page](https://github.com/StephenDsouza90/url-shortner/blob/shortner/screenshots/main.png)

2. Add_url()

In the add_url function, the original long url is stored in the database along with the short url. The short-url route displays the original url and short url to the user.

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