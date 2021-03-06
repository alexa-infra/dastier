from flask import Flask
from database import db_session
from bookmarks import bookmarks_page
from readitlater import readitlater_page
from flask.ext.restless import APIManager
from model import Link, ReadLater

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))

app.register_blueprint(bookmarks_page)
app.register_blueprint(readitlater_page, url_prefix='/readitlater')

manager = APIManager(app, session=db_session)
manager.create_api(Link, methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix='/api', collection_name='bookmark',
                   results_per_page=-1)
manager.create_api(ReadLater, methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix='/api',
                   collection_name='readitlater',
                   results_per_page=20)

@app.teardown_appcontext
def shutdown(error):
    db_session.remove()

