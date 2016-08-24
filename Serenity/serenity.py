# -*- coding: utf-8 -*-
# @Author: zpriddy
# @Date:   2016-08-19 21:21:25
# @Last Modified by:   zpriddy
# @Last Modified time: 2016-08-23 19:41:24

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template("serenity_base.html", title="Base")

@app.route('/devices')
def page2():
  return render_template("devices.html", title="Devices")

@app.route('/d')
def d():
  return render_template('devices.html', title="Devices")

@app.route('/c')
def c():
  return "blah"


if __name__=='__main__':
  app.run(debug=True, host="0.0.0.0", port=8090, threaded=True)