#!/usr/bin/env python

import sys
import datetime


class ReloadLog(object):
	def __init__(self, app=None):
		self.fname = None
		if app:
			self.fname = app.config['RELOAD_LOG']

	def touch_date(self, fn=None):
		fname = fn
		if fname is None:
			fname = self.fname
		try:
			with open(fname, 'a') as f:
				print >> f, datetime.datetime.now()
		except:
			print >> sys.stderr, '[e] touch reload failed.'

if __name__ == '__main__':
	rl = ReloadLog(None)
	rl.touch_date(sys.argv[1])
