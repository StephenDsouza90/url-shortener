import time
import flask
import waitress
import string

from sqlalchemy import Column, String, Integer, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, json, render_template, request, redirect
from random import choices


Base = declarative_base()


class SQLiteBackend(object):
    """ SQLite Backend that manages creating the engine and session """

    def __init__(self, db_creation):
        self.engine = None
        self.Session = sessionmaker(autocommit=False, expire_on_commit=False)
        self.setup_engine(db_creation)

    def setup_engine(self, db_creation=None):
        """ Setup engine, return engine if exist """

        if self.engine:
            return
        self.engine = create_engine(db_creation, echo=False, pool_recycle=3600)
        self.Session.configure(bind=self.engine)

    def bootstrap(self):
        """ Connects to engine and creates tables """

        connection  = None
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
    """ Represents URL database """

    __tablename__ = 'url_database'
    id = Column(Integer(), primary_key=True)
    original_url = Column(String(32), nullable=False)
    short_url = Column(String(5), nullable=False, unique=True)

    def __init__(self, **kwargs):

        # kwargs - passing arugements for columns
        # 11:07 mins .. check again
        super().__init__(**kwargs)

        # generating random char
        self.short_url = self.generate_short_url()

    def generate_short_url(self):
        """ Generate random character randomly and set it to URL """

        char = string.digits + string.ascii_letters
        short_url = ''.join(choices(char, k=5))
        return short_url

        # query short_url incase if it already exist
        # if it already exist then try again
        # session = Session()
        # url = session.query(self).filter_by(short_url=short_url).first()
        # url = self.query.filter_by(short_url=short_url).first()
        # if url:
        #     return self.generate_short_url()


def create_app(db):
    """ Creates the server app """

    app = Flask('URL Shortner')

    # main page
    @app.route('/')
    def main():
        return render_template('main.html')
    
    # stores a long URL and short url in db
    @app.route('/add_url', methods=['POST'])
    def add_url():
        session = db.Session()

        # get original url passed by user
        original_url = request.form['original_url']
        # store url in db
        url = URL(original_url=original_url)
        session.add(url)
        session.commit()
        return render_template('short_url.html', short_url=url.short_url, original_url=url.original_url)

    # redirects short url to original url
    @app.route('/<short_url>')
    def redirect_url(short_url):
        session = db.Session()
        original = session.query(URL).filter_by(short_url=short_url).first()
        if not original:
            return page_not_found(404)
        return redirect(original.original_url) 
        
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error.html'), 404

    return app


def main():
    db_url = "sqlite:///short_url.db"
    print(f'Connecting to {db_url}')
    db = SQLiteBackend(db_url)
    db.bootstrap()
    app = create_app(db)
    waitress.serve(app, host='0.0.0.0', port=8080)


if __name__=='__main__':
    main()

# if original url exist and short urlthen return