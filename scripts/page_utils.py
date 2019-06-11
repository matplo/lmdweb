def safe_meta_get(page, what_meta, default_val=True):
	retval = default_val
	try:
		retval = page.meta.get(what_meta)
	except:
		retval = default_val
		page.meta = { what_meta : default_val}
	if retval is None:
		retval = default_val
		page.meta[what_meta] = default_val
	return retval
