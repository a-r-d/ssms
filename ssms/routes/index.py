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

from ssms.settings import SECRET_KEY, CONFIG_MAP
from ssms.lib.library_utils import list_library

from ssms.lib.entities import openDB
from ssms.lib.entities import getSession
from ssms.lib.entities import UserPrefs, Playlist, PlaylistItem, Bookmark

from ssms.lib.log import log


@app.route('/')
def home( message=None ):
    listing = list_library(CONFIG_MAP['LIB_DIR'], CONFIG_MAP['DB_DIR'])
    bookmark_list = g.db.query(Bookmark).all()
    pl_list = g.db.query(Playlist).all()
    return render_template(
        'home.html', 
        listing=listing,
        bookmarks=bookmark_list,
        playlists=pl_list,
        message=message
    )
