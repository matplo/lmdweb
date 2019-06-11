import page_utils

class MetaInfo(object):
	def __init__(self, pages):
		defaults = [['published', 'True'],
					['title', None],
					['users', 'all'],
					['template', 'page.html'],
					['tags', ['untagged']]]
		for p in pages:
			for minfo in defaults:
				m = minfo[0]
				val = minfo[1]
				if m == 'title':
					val = p.path.replace("/", " ").lstrip()
				page_utils.safe_meta_get(p, m, val)
