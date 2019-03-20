title: Log files
description: A peek to log files...
users: mp
published: 22-11-2016
template: page.html
reload: true
tags: [service]
execs: [ exec.call_cmnd, exec.test, exec.cat_this ]

Test exec.py
===

[exec.call_cmnd()]

[exec.test()]

[exec.cat_this()]

Apache access
===

![exec](date){: raw}
![exec](./scripts/tail_file.sh){: raw args="access.log"}

Apache error
===

![exec](date){: raw}
![exec](./scripts/tail_file.sh){: raw args="error.log"}

App log
===

![exec](date){: raw}
![exec](./scripts/tail_file.sh){: raw args="app.log"}

Reload log
===

![exec](date){: raw}
![exec](./scripts/tail_file.sh){: raw args="reload.log"}
