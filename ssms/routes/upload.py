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
from ssms.lib.library_utils import clean_folder
from ssms.lib.library_utils import list_library
from ssms.lib.library_utils import file_search
from ssms.lib.library_utils import file_search_html
from ssms.lib.library_utils import clean_folder
from ssms.lib.library_utils import allowed_file

from ssms.lib.entities import openDB
from ssms.lib.entities import getSession
from ssms.lib.entities import UserPrefs, Playlist, PlaylistItem, Bookmark

from ssms.lib.log import log


@app.route("/upload/form")
def getUploadForm(message=None):
    if request.method=='GET' and request.args.get("q") != None: 
        loc = request.args.get("q")
        return render_template(
            'uploader_form.html', 
            location=loc,
            message=message
        )
    else:
        return render_template(
            'uploader_form.html', 
            location="",
            message=message
        )

@app.route("/upload/file", methods=['GET', 'POST'])
def postUploadFile(message=None):
    print "Got file upload!"
    try:
        if request.method == 'POST':
            loc = request.form['location']
            print "file loc: ", loc
            if loc == None:
                print "No location set."
                return "Error: no location set"

            file = request.files['files']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print filename
                upload_to = os.path.normpath( CONFIG_MAP['LIB_DIR'] + "/" + loc)
                print "upload to: " + upload_to
                file.save(os.path.join(upload_to, filename))
                listing = list_library(CONFIG_MAP['LIB_DIR'], CONFIG_MAP['DB_DIR'], loc)
                print listing
                return json.dumps( { "files":listing } ) #YAY!
            else:
                return "Filetype not allowed!"
        else:
            return render_template(
                'uploader_form.html', 
                location="",
                message="Nothing Posted!"
            )
    except Exception, e:
        traceback.print_exc()
        print str(e)
        return "error: " + str(e)
