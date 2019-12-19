import time
import flask
import waitress
import string

from random import choices
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, json, render_template, request, redirect


Base = declarative_base()


class SQLiteBackend(object):
    """ SQLite Backend that manages creating the engine and session. """

    def __init__(self, create_db):
        self.engine = None
        self.Session = sessionmaker(autocommit=False, expire_on_commit=False)
        self.setup_engine(create_db)

    def setup_engine(self, create_db=None):
        """ Setup engine, return engine if exist. """

        if self.engine:
            return
        self.engine = create_engine(create_db, echo=False, pool_recycle=3600)
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

        Base.metadata.create_all(self.engine)
        connection.close()


class URL(Base, SQLiteBackend):
    """ Represents URL database. """

    __tablename__ = 'url_database'
    id = Column(Integer(), primary_key=True)
    original_url = Column(String(32), nullable=False)
    short_url = Column(String(5), nullable=False, unique=True)

    def __init__(self, **kwargs):
        """ Extend URL class to generate short url. """

        super().__init__(**kwargs)
        self.short_url = self.generate_short_url()
        
    def generate_short_url(self):
        """ Generate character randomly and set it to be short URL. """

        char = string.digits + string.ascii_letters
        short_url = ''.join(choices(char, k=5))
        """
        # Need to query db to check if short url already exist
        # If the short url exist, try again
        session = self.Session()
        # url = session.query(self).filter_by(short_url=short_url).first()
        # url = self.query.filter_by(short_url=short_url).first()
        if url:
            return self.generate_short_url()
        """
        return short_url


def create_app(db):
    """ Creates server app. """

    app = Flask('URL Shortner')

    @app.route('/')
    def main():
        """ Main page for user to submit url to be shortened. """

        return render_template('main.html')
    
    @app.route('/add_url', methods=['POST'])
    def add_url():
        """ Get original url from user and store it in db along with short url. """

        session = db.Session()

        original_url = request.form['original_url']
        """
        # query if original already exist
        # if original url already exist with short url then return that instead of making a new short url
        ori_url_exist = session.query(URL).filter_by()
        """
        url = URL(original_url=original_url)
        session.add(url)
        session.commit()
        return render_template('short_url.html', short_url=url.short_url, original_url=url.original_url)

    @app.route('/<short_url>')
    def redirect_url(short_url):
        """ Redirects short url to original url. 
            Get original url from querying db. """

        session = db.Session()
        original = session.query(URL).filter_by(short_url=short_url).first()
        if not original:
            return page_not_found(404)
        return redirect(original.original_url) 
        
    @app.errorhandler(404)
    def page_not_found(error):
        """ Return page not found. """

        return render_template('error.html'), 404

    return app


def main():
    """ Creates and connects to db.
        Run server. """
    
    db_url = "sqlite:///short_url.db"
    print(f'Connecting to {db_url}')
    db = SQLiteBackend(db_url)
    db.bootstrap()
    app = create_app(db)
    waitress.serve(app, host='0.0.0.0', port=8080)


if __name__=='__main__':
    main()