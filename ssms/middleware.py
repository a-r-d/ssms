from ssms import app

from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import Response
from flask import send_file
from flask import session
from flask import escape
from flask import g
from werkzeug import secure_filename

# built in:
from datetime import datetime
import os                   # folder opts
import sys                  # for sys.version_info
import socket               # to get hostname
import shutil               # to copy/del folders.
import distutils.core       # to copy tree silently
import subprocess           # to restart server.
import time                 # to wait for server.
import json                 # ajax
import random               # random song.
import urllib2              # for escapeing url encode
import zipfile              # serve folder for download
import traceback            # exception on tough stuff
import sqlite3              # the db

from settings import SECRET_KEY, CONFIG_MAP
from lib.library_utils import clean_folder
from lib.library_utils import list_library
from lib.library_utils import pathMinusLibrary # try to remove this.
from lib.library_utils import find_rand_file
from lib.library_utils import file_search
from lib.library_utils import file_search_html
from lib.library_utils import clean_folder

from lib.entities import openDB
from lib.entities import getSession
from lib.entities import UserPrefs, Playlist, PlaylistItem, Bookmark

from lib.log import log


###########################################################
### DB Layer, and request before + after.
# before, we go and 
@app.before_request
def before_request():
    g.db = get_session()
    #print "req path: " + request.path
    if request.path.startswith("/static") == False and \
        request.path.startswith("/bower_components") == False and \
        request.path.startswith("/login") == False:
        #print "Non static path:"
        if 'user_auth_ok' in session:
            if session['user_auth_ok'] != True:
                return render_template('login_user.html', message="Please Log In!")
        else:
            return render_template('login_user.html',  message="Please Log In!")
    
#close session after request.
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_main_db', None)
    if db is not None:
        db.commit() #close the session.
        
def get_db_session():
    db = getattr(g, '_main_db', None)
    if db is None:
        db = g._database = get_session()
    return db
    
#get session on every request.
def get_session():
    return getSession(CONFIG_MAP['DATABASE'])

