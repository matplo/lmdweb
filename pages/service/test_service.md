title: Test service
subtitle: just a demo
published: True
users: mp
template: service.html
tags: [service]
execs: [ geo_ip.response, get_time.now ]

# Synopsis

Here we just demonstrate the `service` within the pages.

One needs three things:

* an .md file with in `/pages/service` (depending on how the flat pages were configured)
* within the .md file a `execs:` meta that is iterable in a form `module.function` where `module.py` must be present in the `/exec` directory that implements `def function()`
* then within the .md file a string `[module.function()]` gets replaced by the return value of `module.function()`

The difference of this approach and the `![exec](<cmnd>)` is that this one should have the / be within the app context and it really gets executed everytime the page is requested...
On the other hand, reloading the same module is not supported. So once loaded it stays fixed (should be fine for any std use... - in particular one can use configuration files to control behavior of the executed `module::response()` )

# Sample `.md` file

Note the `[` and `]` is escaped below just not to get replaced within *this* file...

```
title: Geo IP
subtitle: check ip origin
published: True
template: service.html
tags: [service]
execs: [ geo_ip.response ]

\[geo_ip.response()\]
```

# Here is the response

`\[geo_ip.response()\]`

[geo_ip.response()]

# Time (server side) within the page...

`\[get_time.now()\]`

Note: again the '[' and ']' are escaped... remove to use the replace functionality

[get_time.now()]

