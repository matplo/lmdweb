title: On markdown
description: Useful tips and notes
users: all
published: 2016-02-07
template: page.html
tags: [demo]

Markdown recommendations - style guide
===

[http://www.cirosantilli.com/markdown-style-guide](http://www.cirosantilli.com/markdown-style-guide){: target="\_"}

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

Inline code
===

Within a line `is this some code`?

---

Codehilite
===

use shebang (for python for example: `#!python`) as a first line of code block for line numbers
```python
class Dummy(object):
    def __init__(self):
        self.more_dummy = None
```

**At the moment the codehilite table adds unnecessary `</div>` to the table with numbers that breaks how the page is rendered with bootstrap, so avoid it where ok to do so...**

[CodeHilite docs](https://pythonhosted.org/Markdown/extensions/code_hilite.html){: class="btn btn-sm btn-warning"}

Images
===

```
![imgx](https://dl.dropboxusercontent.com/u/14190654/web/savegames/IMG_2376.JPG "example picture"){: footer="this is a footer"}
```

![imgx](https://dl.dropboxusercontent.com/u/14190654/web/savegames/IMG_2376.JPG "example picture"){: footer="this is a footer"}

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
