title: Exec snips
description: Just a how-to...
users: somebody, mp
published: 2016-02-07
template: page.html
tags: [mp]

So, this is cool...
===

Execute a `date`
---

# With a `{: raw}` tag

`![exec](date){: raw}`

result

![exec](date){: raw}

# Without the `{: raw}`

![exec](date)

Other examples
---

`![exec](ls -ltr -h){: raw}`
![exec](ls -ltr -h){: raw}

`![exec](./exec/geo_ip.py){: raw}`

![exec](./exec/geo_ip.py){: raw}

`![exec](./exec/geo_ip.py)`

![exec](./exec/geo_ip.py)
