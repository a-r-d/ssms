#-*- coding: utf-8 -*-
# flask app:
from flask import Flask
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

# internal junk
from settings import SECRET_KEY, CONFIG_MAP
from lib.helpers import clean_folder
from lib.helpers import list_library
from lib.helpers import log
from lib.helpers import pathMinusLibrary # try to remove this.
from lib.helpers import find_rand_file
from lib.helpers import file_search
from lib.helpers import file_search_html
from lib.helpers import clean_folder

from lib.entities import openDB
from lib.entities import getSession
from lib.entities import UserPrefs, Playlist, PlaylistItem, Bookmark


# create app:
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = CONFIG_MAP['TEMP_DIR']

# sys.version_info
log("Starting app: " + str(sys.version_info))
log("Application database location: " + CONFIG_MAP['DATABASE'])


## First run setup:
## make temp dirs, logs, ect - all on 'ignore' in the repo..:
for d in CONFIG_MAP['INIT_DIRS']:
    if not os.path.exists(d):
        print "Creating location: " + d
        os.makedirs(d)
        
if not os.path.exists(CONFIG_MAP['DATABASE']):
    print "Creating database at: " + CONFIG_MAP['DATABASE']
    init_db()


##########################################################
### Routes & middlware
###########################################################
import middleware
import routes.index
import routes.auth 
import routes.file

#############################################################
