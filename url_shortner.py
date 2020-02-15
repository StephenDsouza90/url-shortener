import os
import time
import flask
import waitress
import string

from math import floor
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, json, render_template, request, redirect


Base = declarative_base()


class SQLBackend(object):
    """ SQLBackend manages creating
        the engine and session. """

    def __init__(self, db_url):
        self.engine = None
        self.Session = sessionmaker(
            autocommit=False, 
            expire_on_commit=False
            )
        self.setup_engine(db_url)

    def setup_engine(self, db_url=None):
        """ Setup engine, return engine if exist. """

        if self.engine:
            return
        self.engine = create_engine(db_url, 
		echo=False,
		pool_recycle=3600)
        self.Session.configure(bind=self.engine)

    def bootstrap(self):
        """ Connects to engine and creates tables. """

        connection = None
        for i in range(2):
            try:
                connection = self.engine.connect()
            except:
                print("DB Server is not up yet, Retrying..")
                time.sleep(i * 5)
                continue
        if not connection:
            raise Exception("Couldn't connect to DB Server even after retries!")

        Base.metadata.create_all(bind=self.engine)
        connection.close()


class URL(Base):
    """ Represents URL database. """

    __tablename__ = 'url_store'
    id = Column(Integer(), primary_key=True)
    original_url = Column(String(), nullable=False)
    short_url = Column(String())


def generate_short_url(num):
    base = string.digits + string.ascii_letters
    base_len = len(base)

    if base_len <= 0 or base_len > 62:
        return 0
    char = base[num % base_len]
    quotient = floor(num / base_len)
    while quotient:
        mod = quotient % base_len
        quotient = floor(quotient / base_len)
        char = base[mod] + char
    return char


def create_app(db):
    """ Creates server app. """

    app = Flask('URL Shortner')
    
    @app.route('/')
    def main():
        """ Submit a url for shortening. """

        return render_template('main.html')

    def add_original_url():
        """ Add original url in db. """

        session = db.Session()
        original_url = request.form['original_url']
        url = URL(original_url=original_url)
        session.add(url)
        session.commit()
        return url

    def update_short_url(id):
        """ Generate short url and update it in db. """

        session = db.Session()
        short_url = generate_short_url(id)
        session.query(URL).filter(URL.id==id).update(
                    {URL.short_url: short_url}, 
                    synchronize_session=False)
        session.commit()
        return short_url

    @app.route('/short-url', methods=['POST'])
    def get_short_url():
        """ Get original url and short url """

        original_url = add_original_url()
        short_url = update_short_url(original_url.id)
        return render_template(
            'short_url.html', 
            short_url=short_url, 
            original_url=original_url.original_url
            )
       
    @app.errorhandler(404)
    def page_not_found(error):
        """ Return page not found. """

        return render_template('error.html'), 404
    return app


def main():
    """ Creates and connects to db.
        Run server. """

    db = SQLBackend(os.environ.get('DB_URL'))
    print("Connecting to PostgreSQL..")
    db.bootstrap()
    app = create_app(db)
    waitress.serve(app, host='0.0.0.0', port=8080)


if __name__=='__main__':
    main()
