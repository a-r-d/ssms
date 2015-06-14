from ssms import app

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


@app.route('/search/json')
def search( message=None ):
    try:
        res = []
        if request.method=='GET' and request.args.get("q") != None: 
            res = file_search_html(LIB_DIR, request.args.get("q"))
        return json.dumps({"files": res})
    except Exception, e:
        traceback.print_exc()
        log("search error (json): " + str(e) )
        return "search error: " + str(e)


@app.route('/search')
def searchHTML( message=None ):
    try:
        res = []
        if request.method=='GET' and request.args.get("q") != None: 
            res = file_search_html(LIB_DIR, urllib2.unquote(request.args.get("q")))
        return render_template(
            'file_table.html', 
            listing=res,
            message=message
            )
    except Exception, e:
        traceback.print_exc()
        log("search error: " + str(e) )
        return "search error: " + str(e)