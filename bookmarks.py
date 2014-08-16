from flask import Blueprint, render_template, abort, redirect, request, url_for
from sqlalchemy import desc
from database import db_session
from model import Link
from baseconv import base62

bookmarks_page = Blueprint('bookmarks', __name__)

@bookmarks_page.route('/')
def show():
    entries = Link.query.order_by(desc(Link.last_access)).all()
    return render_template('welcome.html', links=entries)

@bookmarks_page.route('/k/<shortcut>')
def follow(shortcut):
    idx = base62.decode(shortcut)
    link = Link.query.filter(Link.id == idx).first()
    if not link:
        abort(404)
    link.touch()
    db_session.add(link)
    db_session.commit()
    return redirect(link.url)

@bookmarks_page.route('/add')
def add():
    url = request.args.get('url')
    title = request.args.get('title')
    if not url or not title:
        abort(400)
    link = Link(url, title)
    db_session.add(link)
    db_session.commit()
    return render_template('add_home.html')

@bookmarks_page.context_processor
def short_url_utility():
    def short_url(idx):
        shortcut = base62.encode(idx)
        return url_for('bookmarks.follow', shortcut=shortcut)
    return dict(short_url=short_url)
