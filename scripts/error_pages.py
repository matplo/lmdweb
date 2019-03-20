from flask import render_template
from flask_flatpages import FlatPages


class ErrorPages(object):
    def __init__(self, app, flatpagesname=None):
        self.app = app
        self.app.error_handler = self
        self.pages = self.app.extensions['flatpages'][flatpagesname]

    def render(self, comment=''):
        print self.pages
        for p in self.pages:
            print 'page:', p
        page             = self.pages.get('service/error')
        ptemplate        = page.meta.get('template', 'page.html')
        navtags          = self.app.navtags
        page.par1 = 'Error comment: {}'.format(comment)
        return render_template(ptemplate, page=page, navtags=navtags)
