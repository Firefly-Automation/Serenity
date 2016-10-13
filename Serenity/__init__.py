# -*- coding: utf-8 -*-
# @Author: Zachary Priddy
# @Date:   2016-08-29 12:03:57
# @Last Modified by:   Zachary Priddy
# @Last Modified time: 2016-10-13 00:36:06

from configparser import ConfigParser
from flask import Flask, render_template


app = Flask(__name__)

config = ConfigParser()
config.read('serenity.config')

fireflyConfig = config['FIREFLY BACKEND']
FF_host = fireflyConfig.get('host','http://localhost')
FF_port = fireflyConfig.getint('port',6001)


serenityConfig = config['SERENITY']
S_host = serenityConfig.get('host', '0.0.0.0')
S_port = serenityConfig.getint('port', 8090)
S_debug = serenityConfig.getboolean('debug', False)

app.config['DEBUG'] = serenityConfig.getboolean('debug', False)

# DATABSE LINK FOR USERS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Serenity.db'
app.config['SECRET_KEY'] = 'super-secret'

app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = 'MyPasswordSalt'

ff_host = FF_host + ':' + str(FF_port)

API_PATHS = {
  'routines' : FF_host + ":" + str(FF_port) + '/API/core/views/routine',
  'mode' : FF_host + ":" + str(FF_port)  + '/API/mode',
  'device_views' : FF_host +  ":" + str(FF_port)  + '/API/core/views/devices',
  'all_device_status' : FF_host + ":" + str(FF_port)  + '/API/core/status/devices/all',
  'command' : FF_host + ":" + str(FF_port)  + '/API/command',
  'alexa' : ff_host + '/API/alexa'
}




import Serenity.models
import Serenity.views