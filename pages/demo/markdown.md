title: Markdown Sandbox
description: Useful tips and notes / cheat sheet
users: all
published: 2016-02-07
template: page.html
tags: [tools]

# References

 - something you want to [link][1] that is a reference.

[1]: http://www.google.com

# On MD
<div class="btn-group-vertical">
[A cheat sheet](https://support.squarespace.com/hc/en-us/articles/206543587-Markdown-cheat-sheet){: class="btn btn-default" target="_blank"}
[MD editors](https://www.shopify.com/partners/blog/10-of-the-best-markdown-editors){: class="btn btn-default" target="_blank"}
[Markdown recommendations - style guide](http://www.cirosantilli.com/markdown-style-guide){: class="btn btn-default" target="_blank"}
</div>

Links
===

 - General note: properties with `{: ...}` is supported

## No buttons

Link to google in a new window: [Google](http://google.com){: target="_blank"}

```
[Google](http://google.com){: target="_blank"}
```

## With buttons

[Default](http://google.com){: class="btn btn-default" target="_blank"}
[Primary](http://google.com){: class="btn btn-primary" target="_blank"}
[Secondary](http://google.com){: class="btn btn-secondary" target="_blank"}
[Success](http://google.com){: class="btn btn-success" target="_blank"}
[Danger](http://google.com){: class="btn btn-danger" target="_blank"}
[Warning](http://google.com){: class="btn btn-warning" target="_blank"}
[Info](http://google.com){: class="btn btn-info" target="_blank"}
[Light](http://google.com){: class="btn btn-light" target="_blank"}
[Dark](http://google.com){: class="btn btn-dark" target="_blank"}
[Link](http://google.com){: class="btn btn-link" target="_blank"}

 - note: some of the above are available from BS 4.x on

```
[Default](http://google.com){: class="btn btn-default" target="_blank"}
[Primary](http://google.com){: class="btn btn-primary" target="_blank"}
[Secondary](http://google.com){: class="btn btn-secondary" target="_blank"}
[Success](http://google.com){: class="btn btn-success" target="_blank"}
[Danger](http://google.com){: class="btn btn-danger" target="_blank"}
[Warning](http://google.com){: class="btn btn-warning" target="_blank"}
[Info](http://google.com){: class="btn btn-info" target="_blank"}
[Light](http://google.com){: class="btn btn-light" target="_blank"}
[Dark](http://google.com){: class="btn btn-dark" target="_blank"}
[Link](http://google.com){: class="btn btn-link" target="_blank"}
```

## Button outline

 - note: available from BS 4.x on

[Primary](http://google.com){: class="btn btn-outline-primary" target="_blank"}

```
[Primary](http://google.com){: class="btn btn-outline-primary" target="_blank"}
```

## Button size

[btn-lg](http://google.com){: class="btn btn-primary btn-lg" target="_blank"}
[normal](http://google.com){: class="btn btn-primary" target="_blank"}
[btn-sm](http://google.com){: class="btn btn-primary btn-sm" target="_blank"}
[btn-xs](http://google.com){: class="btn btn-primary btn-xs" target="_blank"}

```
[btn-lg](http://google.com){: class="btn btn-primary btn-lg" target="_blank"}
[normal](http://google.com){: class="btn btn-primary" target="_blank"}
[btn-sm](http://google.com){: class="btn btn-primary btn-sm" target="_blank"}
[btn-xs](http://google.com){: class="btn btn-primary btn-xs" target="_blank"}
```

## Another way - default target is "_blank"

![blink](google.com)

Inline code
===

Within a line `is this some code`?

```
Within a line `is this some code`?
```

Codehilite
===

use shebang (for python for example: `#!python`) as the first line of code block for line numbers
```python
class Dummy(object):
    def __init__(self):
        self.more_dummy = None
```

**At the moment the codehilite table adds unnecessary `</div>` to the table with numbers that break how the page is rendered with bootstrap, so avoid it where ok to do so...**

[CodeHilite docs](https://pythonhosted.org/Markdown/extensions/code_hilite.html){: class="btn btn-sm btn-warning"}

Images
===

```
![imgx](https://ichef.bbci.co.uk/news/660/cpsprodpb/37B5/production/_89716241_thinkstockphotos-523060154.jpg "example picture"){: footer="this is a footer"}
```

![imgx](https://ichef.bbci.co.uk/news/660/cpsprodpb/37B5/production/_89716241_thinkstockphotos-523060154.jpg "example picture"){: footer="this is a footer"}

![imgx](/img/test.png "/img/test.png"){: footer="this figure is from /static/img directory"}

## Now something without row and using a tag for a collective row...
 - also the `width="<integer">` works

```
![cont](row)
![imgx](/static/Dropbox/EMCAL/2015-EventDisplay/Dec2015/Dijet_3D_2.png){: title="Another local file" footer="More in Dropbox/EMCAL/2015-EventDisplay/Dec2015" width="4" norow="true"}
![imgx](/static/Dropbox/ALICE/AliceED/j_jet_tracks_black.png){: title="Local file" footer="More in Dropbox/ALICE/AliceED" width="4" norow="true"}
![cont](end)
```

![cont](row)
![imgx](/static/Dropbox/EMCAL/2015-EventDisplay/Dec2015/Dijet_3D_2.png){: title="Another local file" footer="More in Dropbox/EMCAL/2015-EventDisplay/Dec2015" width="4" norow="true"}
![imgx](/static/Dropbox/ALICE/AliceED/j_jet_tracks_black.png){: title="Local file" footer="More in Dropbox/ALICE/AliceED" width="4" norow="true"}
![cont](end)


Tables
===

A preference: no starting and ending `|`

Header 1 | Header 2 | Header 3 | Header 4
--- | :-- | :--: | --:
`---` | `:--` | `:--:` | `--:`
default align|left|center|right
*emph*|_or like this_|**bold**|<sub>subscript</sub><sup>superscript</sup>

Source of this is:
```text
Header 1     | Header 2       | Header 3 | Header 4
 ---         | :--            | :--:     | --:
`---`        | `:--`          | `:--:`   | `--:`
default align| left           | center   | right
*emph*       | _or like this_ |**bold**  |<sub>subscript</sub><sup>superscript</sup>
```

Latex with mathjax
===

With [https://www.mathjax.org](https://www.mathjax.org){: target="\_"} and [https://github.com/mitya57/python-markdown-math](https://github.com/mitya57/python-markdown-math){: target="\_"}.

For inline math, use `\(...\)`.

For standalone math, use `$$...$$`, `\[...\]` or `\begin...\end`.

The single-dollar delimiter `($...$)` for inline math is __disabled__ by default, but can be enabled by passing `enable_dollar_delimiter=True` in the extension configuration.

If you want to render to span elements with inline math rather than script elements, so as to improve fallback when JavaScript is disabled or unavailable, use `render_to_span=True`.

Mathjax examples
---

```
$$\alpha_{s}(M_{Z})=0.1184 \pm 0.0007$$
```

$$\alpha_{s}(M_{Z})=0.1184 \pm 0.0007$$

---

```
Something inline is \\( \alpha_{s}(M_{Z})=0.1184 \pm 0.0007 \\).
```

Something inline is \\( \alpha_{s}(M_{Z})=0.1184 \pm 0.0007 \\) .

---

Values from [arxiv:1210.0325](https://arxiv.org/abs/1210.0325){: target="_"}.

Note the link above opens in a new tab because of the `{: target="_}`

```
[arxiv:1210.0325](https://arxiv.org/abs/1210.0325){: target="_"}
```

<div class="row">
  <div class="col-sm-2"></div>
  <div class="col-sm-12">
    <div class="panel panel-info">
      <div class="panel-heading">More on mathjax: static/MathJax/test/sample.html</div>
      <div class="panel-body">
        <div class="embed-responsive embed-responsive-4by3">
          <iframe class="embed-responsive-item" src="/static/MathJax/test/sample.html"></iframe>
        </div>
      </div>
    </div>
  </div>
  <div class="col-sm-2"></div>
</div>

Page in a Panel
===

 - just like above
```html
<div class="row">
  <div class="col-sm-2"></div>
  <div class="col-sm-12">
    <div class="panel panel-info">
      <div class="panel-heading">More on mathjax: static/MathJax/test/sample.html</div>
      <div class="panel-body">
        <div class="embed-responsive embed-responsive-4by3">
          <iframe class="embed-responsive-item" src="/static/MathJax/test/sample.html"></iframe>
        </div>
      </div>
    </div>
  </div>
  <div class="col-sm-2"></div>
</div>
```
