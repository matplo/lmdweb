#!/usr/bin/env python

import datetime as dt


def main():
	t = dt.datetime.now()
	secs = '{:02d}'.format(t.second)
	mins = '{:02d}'.format(t.minute)
	hs   = '{:02d}'.format(t.hour)
	retval = '[ {"h" : "xh", "m" : "xm", "s" : "xs"}]'.replace('xh', hs).replace('xm', mins).replace('xs', secs)
	print retval


def now():
	t = dt.datetime.now()
	return str(t)


if __name__ == '__main__':
	main()
