from flask import Blueprint, render_template, abort, redirect, request, url_for
from sqlalchemy import desc
from database import db_session
from model import Link
from util import truncate_char_to_space

bookmarks_page = Blueprint('bookmarks', __name__)

@bookmarks_page.route('/')
def show():
    entries = Link.query.order_by(desc(Link.last_access)).all()
    return render_template('welcome.html', links=entries)

@bookmarks_page.route('/k/<int:idx>')
def follow(idx):
    link = Link.query.filter(Link.id == idx).first()
    if not link:
        abort(404)
    link.touch()
    db_session.add(link)
    db_session.commit()
    return redirect(link.url)

@bookmarks_page.route('/add')
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
    link = Link(url, title)
    db_session.add(link)
    db_session.commit()
    return render_template('add_home.html')

@bookmarks_page.context_processor
def short_url_utility():
    def short_url(idx):
        return url_for('bookmarks.follow', idx=idx)
    return dict(short_url=short_url)
