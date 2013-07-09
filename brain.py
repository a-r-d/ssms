#-*- coding: utf-8 -*-
# flask app:
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for, redirect
from flask import Response
from flask import send_file
from flask import g

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
import json

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
DATABASE = BASE_DIR + "/db/main.db"
DB_SCHEMA = BASE_DIR + "/db/schema.sql"

LOCAL_DEBUG = False

## make temp dirs, logs, ect - all on 'ignore' in the repo..:
dirs = [TEMP_DIR, LIB_DIR, LOG_DIR, DB_DIR]
for d in dirs:
    if not os.path.exists(d):
        os.makedirs(d)
        
if not os.path.exists(DATABASE):
    init_db()

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
@app.before_request
def before_request():
    g.db = get_db()
    
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_main_db', None)
    if db is not None:
        db.close()
        
    
def get_db():
    db = getattr(g, '_main_db', None)
    if db is None:
        db = g._database = connect_to_db()
    return db
    
def connect_to_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(DB_SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
###########################################################
@app.route('/')
def home( message=None ):
    listing = list_library(LIB_DIR, DB_DIR)
    return render_template(
        'home.html', 
        listing=listing,
        message=message
        )
        
@app.route('/file')
def getFile(message=None ):
    # filename is the absolute path: 
    if request.method=='GET' and request.args.get("q") != None:  
        file = os.path.normpath( LIB_DIR + request.args.get("q") )
        return send_file(file, mimetype="audio/mpeg", as_attachment=False) ## don't send as attachment, serve directly
    else:
        return "Error"
    
@app.route('/dir')
def getDirHTML( message=None ):
    listing = []
    if request.method=='GET' and request.args.get("q") != None: 
        listing = list_library(LIB_DIR, DB_DIR, request.args.get("q"))
    return render_template(
        'file_table.html', 
        listing=listing,
        message=message
        )
 
@app.route('/dir/json')
def getDirJSON( message=None ):
    listing = []
    if request.method=='GET' and request.args.get("q") != None: 
        listing = list_library(LIB_DIR, DB_DIR, request.args.get("q"))
    return json.dumps( listing )

    
@app.route('/admin')
def adminPanel():
    return render_template(
        'admin.html', 
        message=message
        )

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
