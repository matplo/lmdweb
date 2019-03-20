import importlib
import sys
import os


def exists_in_syspath(fname):
	for s in sys.path:
		if os.path.exists(os.path.join(s, fname)):
			return True
	return False


class ExecService(object):
	def __init__(self, execs, page_rendered, prerender_jinja):
		self.ret_page_rendered = page_rendered
		if execs:
			# print execs
			for px in execs:
				# print px
				modname = 'exec.{}'.format(px.split('.')[0])
				fname = modname.replace('.', '/') + '.py'
				extst = exists_in_syspath(fname)
				# print 'exists?', modname, fname, extst
				if extst:
					mod = importlib.import_module(modname)
					funcname = px.split('.')[1]
					# print 'module is:', mod, funcname
					response = getattr(mod, funcname)()
					response = response.strip('\n')
					# print response
					prj = prerender_jinja(response)
					self.ret_page_rendered = self.ret_page_rendered.replace('[{}()]'.format(px), prj)

	def rendered(self):
		return self.ret_page_rendered
