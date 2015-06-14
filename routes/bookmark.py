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


######### bookmarks ########################################################
@app.route("/bookmark/new")
def mkNewBookmark(message=None):
    if request.method=='GET' and request.args.get("location") != None and request.args.get("name") != None: 
        loc = request.args.get("location")
        name = request.args.get("name")
        new_mark = Bookmark(name, loc, 100)
        g.db.add( new_mark )
        bookmark_list = g.db.query(Bookmark).all()
        g.db.commit()
        return render_template(
            'bookmark_list.html', 
            bookmarks=bookmark_list,
            message=message
        )
    else:
        return "fail"

@app.route("/bookmark/del")
def delBookmark(message=None):
    if request.method=='GET' and request.args.get("id") != None: 
        id = request.args.get("id")

        entry = g.db.query(Bookmark).filter_by(id=id).first() 
        g.db.delete( entry )
        g.db.commit()

        return render_template(
            'bookmark_list.html', 
            message=message
        )
    else:
        return "fail"