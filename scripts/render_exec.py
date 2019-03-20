#!/usr/bin/env python

from HTMLParser import HTMLParser
from utils import text_between, call_exec
import prerender
# https://docs.python.org/2/library/htmlparser.html
# create a subclass and override the handler methods


class RIMGHTMLParser(HTMLParser):
	tagstr = 'img'

	def __init__(self, *args, **kwargs):
		# super(HTMLParser, self).__init__(*args, **kwargs)
		HTMLParser.__init__(self)
		self.is_tag = False
		self.attrs = []

	def handle_starttag(self, tag, attrs):
		if tag == self.tagstr:
			# print "[i] Encountered a start tag:", tag, attrs
			# print "    Attributes:",attrs
			self.is_tag = True
			self.attrs.append(dict(attrs))  # store only attributes

	def handle_endtag(self, tag):
		if tag == self.tagstr:
			# print "    Encountered an end tag :", tag
			self.is_tag = False

	def handle_data(self, data):
		if self.is_tag is True:
			# print "    Data is:",data
			pass
			# note we ignore the data; this tag should have none

	def get_attr(self, what, attrs=None):
		if attrs is None:
			attrs = self.attrs[0]
		try:
			return attrs[what]
		except:
			return ''

	def render_tag(self, i=0):
		if len(self.attrs) <= 0:
			return ''
		exec_arr = []
		exec_arr.append(self.get_attr('src', self.attrs[i]))
		# args = self.get_attr('title', self.attrs[i]).split(' ')
		# for s in args:
		# 	exec_arr.append(s)
		outs = ' '.join(exec_arr)
		return outs


def skip_codehilite(text):
	# this is not needed - codehilite run before does the job => no html recognizible things...
	return text


def get_exec(text):
	p = RIMGHTMLParser()
	p.feed(text)
	p.close()
	return p.render_tag()


# for better pasing see: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
def render_exec(text):
	starts = '<img alt="exec"'
	ends   = ' />'
	srepl = text_between(text, starts, ends)
	print 'to be replaced:', srepl
	while len(srepl) > 0:
		p = RIMGHTMLParser()
		p.feed(text)
		p.close()
		exec_script = p.render_tag()
		sargs = p.get_attr('args')
		if sargs:
			exec_script = exec_script + ' ' + sargs
		if exec_script[:2] == './':
			cdir = '{}/'.format(prerender.gRenderer.app.config['APP_DIR'])
			exec_script = exec_script.replace('./', cdir)
		print 'exec script:', exec_script
		result_script = call_exec(exec_script, ' ')
		# print result_script
		if p.get_attr('raw'):
			print '[i] attribute raw present...'
			stmp = '```\n{}\n```\n'.format(result_script)
			result_script = prerender.prerender_jinja_codehilite(stmp)
		else:
			if p.get_attr('md'):
				print '[i] attribute md present...'
				result_script = prerender.prerender_jinja_md(result_script)

		if result_script is None:
			result_script = '[{}=>None]'.format(exec_script)
		# print srepl, result_script
		text = text.replace(srepl, result_script)
		srepl = text_between(text, starts, ends)
	return text


def main():
	test = 'ala ma kota <img alt="exec" footer="This is a footer" src="ls -ltr" title="Title set from .md file" width="4" /> a kot ma ale'
	# p = RIMGHTMLParser()
	# p.feed(test)
	# p.close()
	# print p.render_tag()
	print render_exec(test)

if __name__ == '__main__':
	main()
