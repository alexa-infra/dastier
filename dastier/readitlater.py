from flask import Blueprint, abort, render_template, request, url_for
from database import db_session
from model import ReadLater
from util import truncate_char_to_space

readitlater_page = Blueprint('readitlater', __name__)

@readitlater_page.route('/')
def show():
    return render_template('readlater.html')

@readitlater_page.route('/add')
def add():
    if not 'url' in request.args or not 'title' in request.args:
        abort(400)
    url = request.args.get('url')
    title = request.args.get('title')
    url = url.strip()
    title = title.strip()
    if not title:
        title = url
    title = truncate_char_to_space(title, 50)
    link = ReadLater(url, title)
    db_session.add(link)
    db_session.commit()
    return render_template('add_read_later.html')

