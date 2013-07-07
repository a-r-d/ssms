#-*- coding: utf-8 -*-
# flask app:
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for, redirect
from flask import Response
from flask import send_file

# built in:
from datetime import datetime
import os 
import glob
import socket # to get hostname
import zipfile #to deal with war file
import shutil # to copy/del folders.
import distutils.core #to copy tree silently
import subprocess # to restart server.
import time # to wait for server.

#external libs:
import sqlite3

# internal junk
from helpers import clean_folder
from helpers import list_library
from helpers import log

###########################################################
# get the dir name to be relative to.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = BASE_DIR + "/temp"
LIB_DIR = BASE_DIR + "/library"
LOG_DIR = BASE_DIR + "/logs"
LOG_FILE = LOG_DIR + "/out.log"
DB_DIR = BASE_DIR + "/db"
DB_FILE = BASE_DIR + "/db/main.db"

LOCAL_DEBUG = False

## make temp dirs, logs, ect - all on 'ignore' in the repo..:
dirs = [TEMP_DIR, LIB_DIR, LOG_DIR, DB_DIR]
for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)

# create app:
app = Flask(__name__)

###########################################################
"""

Default templating is jinja2:
http://jinja.pocoo.org/docs/templates/

Default port for Flask is 5000

Notable static files:
url_for('static', filename='custom.css')
url_for('static', filename='custom.js')
url_for('static', filename='bootstrap_readable.min.css')
url_for('static', filename='jquery-1.9.1.min.js')

"""

###########################################################
@app.route('/')
def home( message=None ):
    listing = list_library(LIB_DIR, DB_DIR)
    return render_template(
        'home.html', 
        listing=listing,
        message=message
        )
@app.route('/file/<filename>')
def getFile( filename, message=None ):
    # filename is the absolute path: 
    
    file = os.path.join( LIB_DIR, filename )
    
    return send_file(file, mimetype="audio/mpeg", as_attachment=False) ## don't send as attachment, serve directly

############################################################################
# end routes
############################################################################
#############################################################
if __name__ == '__main__':
    print "starting in: " + BASE_DIR
    if socket.gethostname() == "waffles":
        LOCAL_DEBUG = True
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')
