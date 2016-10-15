# -*- coding: utf-8 -*-
# @Author: Zachary Priddy
# @Date:   2016-08-29 12:06:24
# @Last Modified by:   Zachary Priddy
# @Last Modified time: 2016-10-14 18:01:19

from Serenity import *

if S_debug:
  app.run(host=S_host, port=S_port, threaded=True)

else:
  from gevent.wsgi import WSGIServer
  http_server = WSGIServer((S_host, S_port), app)
  http_server.serve_forever()
