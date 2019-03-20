import markdown
from imgx_responsive_html import render_imgx
from flask import render_template_string, Markup
from root_plot_html import render_rootjs
from render_exec import render_exec

gRenderer = None


class Renderer(object):
	def __init__(self, app, flatpagesname=None):
		self.app = app
		if flatpagesname is None:
			extname = 'FLATPAGES_MARKDOWN_EXTENSIONS'
		else:
			extname = '_'.join(flatpagesname, 'FLATPAGES_MARKDOWN_EXTENSIONS')
		self.markdown_extensions = app.config[extname]
		# print '[i] Renderer with mdown extensions {}'.format(str(self.markdown_extensions))
		app.config.update(FLATPAGES_HTML_RENDERER=prerender_jinja)
		global gRenderer
		gRenderer = self


def table_bootstrap(shtml):
	shtml = shtml.replace('<table>', '<div class="table-responsive"><table class="table">')
	shtml = shtml.replace('</table>', '</table></div>')
	return shtml


def header_h1_well(htmlpage):
	htmlpage = htmlpage.replace('<h1 id=', '</div> <div class="well well-sm"> <h1 id=')
	htmlpage = htmlpage.replace('</h1>', '</h1><hr>')
	return htmlpage


def prerender_jinja(body=''):
	global gRenderer
	body = render_template_string(Markup(body))
	body = markdown.markdown(body, extensions=gRenderer.markdown_extensions)
	body = render_exec(body)
	body = render_rootjs(body)
	body = render_imgx(body)
	body = table_bootstrap(body)
	body = header_h1_well(body)
	return body

def prerender_jinja_md(body=''):
	global gRenderer
	body = markdown.markdown(body, extensions=gRenderer.markdown_extensions)
	body = render_exec(body)
	body = render_rootjs(body)
	body = render_imgx(body)
	body = table_bootstrap(body)
	body = header_h1_well(body)
	return body


def prerender_jinja_codehilite(body=''):
	body = render_template_string(Markup(body))
	body = markdown.markdown(body, extensions=['codehilite', 'fenced_code'])
	return body
