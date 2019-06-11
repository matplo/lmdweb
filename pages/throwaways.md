title: Throwaways
description: a collection of interesting things...
users: mp
published: someday
template: page.html
tags: [tools,mp]

# removed from the index_base.html

 - before moving scripts local

## mathjax configuration

```html
		<script src="{{url_for('static', filename='MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML')}}"></script>
		<!-- <script type="text/javascript"
			async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
		</script> -->
		<script type="text/x-mathjax-config">
		MathJax.Hub.Config({
		  config: ["MMLorHTML.js"],
		  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
		  extensions: ["MathJax/MathMenu.js", "MathZoom.js"]
		});
		</script>
```

## jinja statements

 - both in scripts block and styles - removed `{ { super() } }` - typo (extra spaces) for obvious reasons

# options to bootstrap:
 - use the extra -theme with

```html
<link rel="stylesheet" href="{{ url_for('static', filename='node_modules/bootstrap/dist/css/bootstrap.min.css') }}">
```