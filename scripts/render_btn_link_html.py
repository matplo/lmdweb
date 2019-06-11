#!/usr/bin/env python

from HTMLParser import HTMLParser
from utils import text_between

# https://docs.python.org/2/library/htmlparser.html
# create a subclass and override the handler methods


class IMGHTMLParser(HTMLParser):
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

	def calculate_width(self, hint):
		ihint = 8
		if len(hint) < 1:
			return [2, 8]
		try:
			ihint = int(hint)
		except:
			ihint = 8
		low_hint = (12 - ihint) / 2
		high_hint = ihint
		while low_hint * 2 + high_hint < 12:
			high_hint += 1
		while low_hint * 2 + high_hint > 12:
			high_hint -= 1
		return [low_hint, high_hint]

	def render_tag(self, i=0):
		if len(self.attrs) <= 0:
			return ''
		_link = self.get_attr('src', self.attrs[i])
		if not _link:
			_link = '?bad link?'
		_text = self.get_attr('text', self.attrs[i])
		if not _text:
			_text = _link
		_class = self.get_attr('class', self.attrs[i])
		if not _class:
			_class = 'class="btn btn-default"'
		else:
			_class = 'class="{}"'.format(_class)
		outs = '[{}]({}){}'.format(_text, _link, '{: '+_class+' target="_blank"}')
		return outs


def skip_codehilite(text):
	# this is not needed - codehilite run before does the job => no html recognizible things...
	return text


def render_blink(text):
	p = IMGHTMLParser()
	p.feed(text)
	p.close()
	return p.render_tag()


# for better pasing see: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
def render_container(text):
	out   = []
	starts = '<img alt="blink"'
	ends   = ' />'
	srepl = text_between(text, starts, ends)
	while srepl != '':
		text = text.replace(srepl, render_blink(srepl))
		srepl = text_between(text, starts, ends)
	return text


def main():
	test = 'ala ma kota <img alt="blink" class="btn" footer="This is a footer" src="google.com" title="Title set from .md file" width="4" /> a kot ma ale '
	# p = RIMGHTMLParser()
	# p.feed(test)
	# p.close()
	# print p.render_tag()
	print render_container(test)

if __name__ == '__main__':
	main()
