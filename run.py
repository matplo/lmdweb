#!/usr/bin/env python

import sys
import scandir
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
from scripts.meta import MetaInfo
from scripts.navigation import NavTags
from scripts.auth import Authentication
from scripts.reload_log import ReloadLog
from scripts.exec_service import ExecService
import scripts.userdb as userdb
from scripts.log import setup_logger
from functools import wraps
import json
import string

def mywalk(root):
    return scandir.walk(root, followlinks=True)
os.walk = mywalk

thisdir    = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(thisdir, 'contents'))
sys.path.insert(0, os.path.join(thisdir, 'pages'))
sys.path.insert(0, thisdir)
configfile = os.path.join(thisdir, 'config/default')

app = Flask(__name__)
app.config['APP_DIR'] = thisdir
app.config['RELOAD_LOG'] = os.path.join(app.config['APP_DIR'], 'logs/reload.log')
config = AppConfig(app, configfile)
Bootstrap(app)
Session(app)
setup_logger(app)
renderer    = Renderer(app)
pages       = FlatPages(app)
MetaInfo(pages)
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
    pages.reload()
    MetaInfo(pages)
    return redirect('/public/index')


@app.route('/<path:path>/', methods=['GET', 'POST'])
def page(path):
    page             = pages.get_or_404(path)
    ptemplate        = page.meta.get('template', 'page.html')
    if auth.user_authorized(session['user'], page) is False:
        next_url = '/{}/'.format(path)
        return redirect(url_for('logon', next=next_url))
    edit_flag = request.args.get('edit')
    if edit_flag:
        fname = os.path.join(pages.root, page.path + app.config['FLATPAGES_EXTENSION'])
        # s = render_template('edit_page_with_quill.html', ppath=fname, contents=page, navtags=navtags)
        s = render_template('edit_page.html', ppath=fname, contents=page, navtags=navtags)
        with open(fname) as f:
            clines = f.readlines()
        # s = s.replace('<_edit_raw_contents_>', ''.join(clines).replace("'", "\'").replace('\n', '\\n'))
        # s = s.replace('<_edit_raw_contents_>', 'some other file contents')
        # st = ''.join(clines).replace("\\", "\\\\").replace("'", "\'").replace('\n', '\\n')
        clines_ascii = []
        for c in clines:
            l = fix_ascii(c)
            clines_ascii.append(l)
        st = ''.join(clines_ascii)
        s = s.replace('<_edit_raw_contents_>', st)
        return s
    return render_template(ptemplate, page=page, navtags=navtags)


@app.errorhandler(404)
def page_not_found(e):
    # print 'not found', e
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


def fix_ascii(s):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, s))


@app.route('/submitedit', methods=['POST'])
@requires_auth
def submit_edit():
    sjson = json.loads(request.form['doc'])
    out = []
    # print sjson
    try:
        out.append(sjson['edit'])
    except:
        pass
    ppath = fix_ascii(sjson['path'])
    sreload = '/' + str(ppath)
    outfname = os.path.join(os.getcwd(), 'pages', ppath + '.md')
    outfname = fix_ascii(outfname)
    # print sjson['new']
    if sjson['new'] == 'yes':
        if os.path.exists(outfname):
            return redirect(sreload)
    with open(outfname, 'w') as f:
        sall = ''.join(out)
        suni = fix_ascii(sall)
        f.write(suni)
    pages.reload()
    MetaInfo(pages)
    # print '[i] written', outfname, sreload
    return redirect(sreload)


def submit_edit_quill():
    sjson = json.loads(request.form['doc'])
    out = []
    # print sjson
    for e in sjson['edit']['ops']:
    	try:
    		out.append(e['insert'])
    	except:
    		pass
    ppath = sjson['path']
    outfname = os.path.join(os.getcwd(), 'pages', ppath + '.md')
    with open(outfname, 'w') as f:
        f.write(''.join(out))
    pages.reload()
    sreload = '/' + str(ppath)
    # print '[i] written', outfname, sreload
    return redirect(sreload)


@app.route('/receivedata', methods=['POST'])
def receive_data():
    print request.form['myData']
    return request.form['myData']


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
    edit_flag = request.args.get('edit')
    if edit_flag:
        fname = os.path.join(pages.root, page.path + app.config['FLATPAGES_EXTENSION'])
        s = render_template('edit_page.html', ppath=fname, contents=page, navtags=navtags)
        with open(fname) as f:
            clines = f.readlines()
        clines_ascii = []
        for c in clines:
            l = fix_ascii(c)
            clines_ascii.append(l)
        st = ''.join(clines_ascii)
        s = s.replace('<_edit_raw_contents_>', st)
        return s
    ptemplate = page.meta.get('template', 'page.html')
    page_rendered = render_template(ptemplate, page=page, navtags=navtags)
    exs = ExecService(page.meta.get('execs'), page_rendered, prerender_jinja)
    page_rendered = exs.rendered()
    return page_rendered


if __name__ == '__main__':
    efiles = []
    efiles.append(app.config['RELOAD_LOG'])
    if '--dev' in sys.argv:
        app.run(debug=True, extra_files=efiles)
    else:
        from waitress import serve
        serve(app, listen='*:8420')
