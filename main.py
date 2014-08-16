from flask import Flask, url_for, request
from database import db_session
from bookmarks import bookmarks_page
from readitlater import readitlater_page

app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.add_extension('spaceless.SpacelessExtension')

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='alex',
    PASSWORD='qwe123'
))

app.register_blueprint(bookmarks_page)
app.register_blueprint(readitlater_page, url_prefix='/readitlater')

@app.teardown_appcontext
def shutdown(error):
    db_session.remove()

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)


