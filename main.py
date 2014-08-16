from flask import Flask, g, render_template, url_for, abort, redirect, request
from database import db_session
from model import Link, ReadLater
from baseconv import base62
import datetime
from sqlalchemy import desc
from pagination import Pagination

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.add_extension('spaceless.SpacelessExtension')

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='alex',
    PASSWORD='qwe123'
))

@app.teardown_appcontext
def shutdown(error):
    db_session.remove()

@app.route('/')
def show_welcome():
    entries = Link.query.order_by(desc('last_access')).all()
    return render_template('welcome.html', links=entries)

@app.route('/k/<shortcut>')
def follow(shortcut):
    idx = base62.decode(shortcut)
    link = Link.query.filter(Link.id == idx).first()
    if not link:
        abort(404)
    link.usage_count += 1
    link.last_access = datetime.datetime.utcnow()
    db_session.add(link)
    db_session.commit()
    return redirect(link.url)

@app.route('/add_home')
def add_home():
    url = request.args.get('url')
    title = request.args.get('title')
    if not url or not title:
        abort(400)
    link = Link(url, title)
    db_session.add(link)
    db_session.commit()
    return render_template('add_home.html')

PER_PAGE = 20

@app.route('/readlater/', defaults={'page': 1})
@app.route('/readlater/page/<int:page>')
def show_realater(page):
    query = ReadLater.query.filter(ReadLater.readed == False) \
                           .order_by(desc(ReadLater.created))
    count = query.count()
    items = query.limit(PER_PAGE).offset(PER_PAGE * (page - 1))
    if not items and page != 1:
        abort(404)
    paginator = Pagination(page, PER_PAGE, count)
    return render_template('readlater.html', links=items,
                           paginator=paginator)

@app.route('/add_readlater')
def add_readlater():
    url = request.args.get('url')
    title = request.args.get('title')
    if not url or not title:
        abort(400)
    link = ReadLater(url, title)
    db_session.add(link)
    db_session.commit()
    return render_template('add_home.html')

@app.context_processor
def short_url_utility():
    def short_url(idx):
        shortcut = base62.encode(idx)
        return url_for('follow', shortcut=shortcut)
    return dict(short_url=short_url)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)


