import markdown

from HTMLParser import HTMLParser

# https://docs.python.org/2/library/htmlparser.html
# create a subclass and override the handler methods


class MyHTMLParser(HTMLParser):
	def __init__(self, *args, **kwargs):
		# super(HTMLParser, self).__init__(*args, **kwargs)
		HTMLParser.__init__(self)
		self.is_h1 = False
		self.h1_attr = ''
		# self.sections = [['#', 'top']]
		self.sections = []

	def handle_starttag(self, tag, attrs):
		if tag == 'h1':
			# print "Encountered a start tag:", tag, attrs
			self.is_h1 = True
			for a in attrs:
				if a[0]=='id':
					self.h1_attr = a[1]

	def handle_endtag(self, tag):
		if tag == 'h1':
			# print "Encountered an end tag :", tag
			self.is_h1 = False

	def handle_data(self, data):
		if self.is_h1 is True:
			if data[0] != '!':
				# print 'Data:',data
				self.sections.append([self.h1_attr, data])


class PTag(object):
	def __init__(self, name):
		self.name 	= name
		self.pages 	= []
		self.path 	= None

	def add_page(self, page):
		self.pages.append(page)


class NavTags(object):
	def __init__(self, app, flatpagesname=None):
		self.app       = app
		self.all_pages = app.extensions['flatpages'][flatpagesname]
		self.pages     = [p for p in self.all_pages if p.meta.get('published')]
		self.tags      = []
		self._pages_to_tags()
		self.app.navtags   = self

	def filter_for_user(self, user):
		tmppages = [p for p in self.all_pages if p.meta.get('published')]
		self.pages = []
		for p in tmppages:
			if self.app.auth.user_authorized(user, p):
				self.pages.append(p)
		self.tags      = []
		self._pages_to_tags()

	def sections(self, p):
		try:
			body = p.body
		except:
			return []
		mdown = markdown.markdown(body, extensions=['codehilite', 'fenced_code', 'tables', 'attr_list', 'toc'])
		# here parse the page with html parser
		# extract the <h1> text
		parser = MyHTMLParser()
		parser.feed(mdown)
		#print '[i] tags for',p,parser.sections
		return parser.sections

	def toc(self, p):
		try:
			body = p.body
		except:
			return None
		md = markdown.Markdown(extensions=['fenced_code', 'toc'])
		html = md.convert(body)
		#page = render_some_template(context={'body': html, 'toc': md.toc})
		toc = md.toc
		toc = toc.replace('<ul>', '').replace('</ul>', '')
		toc = toc.replace('<div class="toc">', '<ul class="dropdown-menu scrollable-menu" role="menu">').replace('</div>', '</ul>')
		#print 'toc for',p,toc
		if '<li' not in toc:
			return None
		else:
			return toc

	def tag_names(self):
		names = []
		for t in self.tags:
			names.append(t.name)
		return names

	def get_tag(self, name):
		for t in self.tags:
			if t.name == name:
				return t
		return None

	def _pages_to_tags(self):
		for p in self.pages:
			taglist = p.meta.get('tags', [])
			for t in taglist:
				tp = self.get_tag(t)
				if tp == None:
					newptag = PTag(t)
					self.tags.append(newptag)
				tp = self.get_tag(t)
				tp.add_page(p)

	def __repr__(self):
		outs = []
		for t in self.tags:
			outs.append(t.name)
			outs.append( ', '.join([p.meta.get('title', []) for p in t.pages]) )
		return '\n'.join(outs)

