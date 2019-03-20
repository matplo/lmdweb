import sys
import os
from flask import Flask, render_template, request, redirect, session, escape, url_for, flash, g
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension
from flask_flatpages import FlatPages, pygmented_markdown, pygments_style_defs
from scripts import logon_form, geo_ip
from scripts.page_process import Section
from scripts.utils import call_exec
from scripts.error_pages import ErrorPages
from scripts.prerender import Renderer, prerender_jinja
from scripts.navigation import NavTags
from scripts.auth import Authentication
from scripts.reload_log import ReloadLog
from scripts.exec_service import ExecService
import scripts.userdb as userdb
from scripts.log import setup_logger
from functools import wraps

thisdir    = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(thisdir, 'contents'))
configfile = os.path.join(thisdir, 'config/default')

app = Flask(__name__)
app.config['APP_DIR'] = thisdir
app.config['RELOAD_LOG'] = os.path.join(app.config['APP_DIR'], 'logs/reload.log')
AppConfig(app, configfile)
Bootstrap(app)
Session(app)
setup_logger(app)
renderer    = Renderer(app)
pages       = FlatPages(app)
auth        = Authentication(app)
navtags     = NavTags(app)
error_pages = ErrorPages(app)
toolbar     = DebugToolbarExtension(app)
reload_log  = ReloadLog(app)
reload_log.touch_date()

dbdir = os.path.join(thisdir, 'hash')
userdb.gUsers = userdb.Users(dbdir)

app.add_url_rule('/static/<path:filename>',
                 endpoint='static',
                 subdomain='',
                 view_func=app.send_static_file)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            session['user'].valid
        except:
            return redirect(url_for('logon'))
        return f(*args, **kwargs)
    return decorated


# # preps
@app.before_request
def before_request():
    try:
        session['user'].valid
    except:
        session['user'] = None
    navtags.filter_for_user(session['user'])


@app.route('/')
@app.route('/index')
def index():
    return redirect('/public/index')


@app.route('/<path:path>/')
def page(path):
    page             = pages.get_or_404(path)
    ptemplate        = page.meta.get('template', 'page.html')
    if auth.user_authorized(session['user'], page) is False:
        next_url = '/{}/'.format(path)
        return redirect(url_for('logon', next=next_url))
    return render_template(ptemplate, page=page, navtags=navtags)


@app.errorhandler(404)
def page_not_found(e):
    print 'not found', e
    page             = pages.get('service/error')
    ptemplate        = page.meta.get('template', 'page.html')
    return render_template(ptemplate, page=page, navtags=navtags), 404


@app.route('/tag/<string:tag>/')
def tag(tag):
    published = [p for p in pages if p.meta.get('published')]
    tagged = [p for p in published if tag in p.meta.get('tags', [])]
    return render_template('tag.html', tagged_pages=tagged, tag=tag, navtags=navtags)


@app.route('/logon', methods=['GET', 'POST'])
def logon():
    try:
        session.pop('user')
    except:
        pass
    userdb.gUsers.load()
    jumbo = {'head': 'Logon page', 'text': 'No text to add...'}
    form = logon_form.PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            fentry = request.form['password']
            fentries = []
            try:
                fentries = fentry.split('/')
            except:
                pass
            while len(fentries) < 2:
                fentries.append('')
            if auth.check_auth(fentries[0], fentries[1]):
                session['user'] = userdb.gUsers.find_user(fentries[0])
                # print 'next:', request.args.get("next")
                # print 'referer:', request.referrer
                return redirect(request.args.get("next") or url_for("index"))
            if len(fentry) < 1:
                form.password.errors.insert(0, '...this is not really a password, is it?')
            else:
                form.password.errors.insert(0, 'unable to authenticate...')
    return render_template('logon.html', jumbo=jumbo, form=form)


@app.route('/logout')
def logout():
    userdb.gUsers.load()
    try:
        session.pop('user')
    except:
        pass
    return redirect(url_for('index'))


@app.route('/img')
@app.route('/img/<var>')
def img(var=''):
    basename = thisdir + '/static/img/'
    fname    = basename + var
    retval = 'No Image'
    try:
        with open(fname) as f:
            retval = f.read()
    except:
        retval = 'Unable to read from: {}'.format(fname)
    return retval


@app.route('/data')
@app.route('/data/<var>')
def data(var=''):
    basename = thisdir + '/static/data/'
    fname = basename + var
    lines = '[ {"data" : "xx"} ]'.replace('xx', fname.replace(basename, ''))
    try:
        with open(fname) as f:
            lines = f.read()
    except:
        pass
    return lines


@app.route('/exec')
@app.route('/exec/<var>')
@requires_auth
def execute(var=''):
    scall = os.path.join(os.path.abspath(os.path.curdir), 'contents/exec/{}.py'.format(var))
    retval = call_exec(scall)
    if retval is None:
        # retval = ErrorPage('Tried: query/' + var, 401).render()
        retval = error_pages.render('executing {}'.format(var))
    return retval


@app.route('/service/<string:tag>/')
def service(tag):
    page = pages.get_or_404('service/{}'.format(tag))
    if auth.user_authorized(session['user'], page) is False:
        next_url = '/service/{}'.format(tag)
        return redirect(url_for('logon', next=next_url))
    if page.meta.get('reload'):
        reload_log.touch_date()
        pages.reload()
        page = pages.get_or_404('service/{}'.format(tag))
    ptemplate = page.meta.get('template', 'page.html')
    page_rendered = render_template(ptemplate, page=page, navtags=navtags)
    exs = ExecService(page.meta.get('execs'), page_rendered, prerender_jinja)
    page_rendered = exs.rendered()
    return page_rendered


if __name__ == '__main__':
    efiles = []
    efiles.append(app.config['RELOAD_LOG'])
    # app.run(debug=app.debug, extra_files=efiles)
    from waitress import serve
    serve(app, listen='*:8420')
