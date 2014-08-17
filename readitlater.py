from flask import Blueprint, abort, render_template, request, url_for
from sqlalchemy import desc
from database import db_session
from model import ReadLater
from pagination import Pagination
from util import truncate_char_to_space

readitlater_page = Blueprint('readitlater', __name__)

PER_PAGE = 20

@readitlater_page.route('/', defaults={'page': 1})
@readitlater_page.route('/page/<int:page>')
def show(page):
    query = ReadLater.query.order_by(desc(ReadLater.created))
    count = query.count()
    items = query.limit(PER_PAGE).offset(PER_PAGE * (page - 1))
    if not items and page != 1:
        abort(404)
    paginator = Pagination(page, PER_PAGE, count)
    return render_template('readlater.html', links=items,
                           paginator=paginator)

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

@readitlater_page.app_template_global()
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

