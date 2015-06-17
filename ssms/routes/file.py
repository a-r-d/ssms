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
from ssms.lib.library_utils import pathMinusLibrary # try to remove this.
from ssms.lib.library_utils import find_rand_file
from ssms.lib.library_utils import file_search
from ssms.lib.library_utils import file_search_html
from ssms.lib.library_utils import clean_folder

from ssms.lib.entities import openDB
from ssms.lib.entities import getSession
from ssms.lib.entities import UserPrefs, Playlist, PlaylistItem, Bookmark

from ssms.lib.log import log

###
@app.route('/file') 
def getFile(message=None ):
    # filename is the absolute path: 
    if request.args.get("q") != None:  
        path = os.path.normpath( CONFIG_MAP['LIB_DIR'] + urllib2.unquote(request.args.get("q")))
        #print "Serving file: ", path
        return send_file(path, mimetype="audio/mpeg", as_attachment=False) ## don't send as attachment, serve directly
    else:
        return "Error"

@app.route('/file/download')
def getFileDownload(message=None ):
    if request.args.get("q") != None:  
        the_path = os.path.normpath( CONFIG_MAP['LIB_DIR'] + urllib2.unquote( request.args.get("q")) )
        return send_file(the_path, mimetype="audio/mpeg", as_attachment=True)
    else:
        return "Error"

@app.route('/file/delete')
def deleteFile(message=None ):
    if session.get("admin_auth_ok") == False:
        return "User not authorized"
    if request.args.get("name") != None:  
        the_path = os.path.normpath( CONFIG_MAP['LIB_DIR'] + urllib2.unquote( request.args.get("name")) )
        if os.path.isdir( the_path ):
            return "Can't delete directory."
        else:
            os.unlink( the_path )
            return "ok"
    else:
        return "Error"
    
@app.route('/dir', methods=['POST'])
def getDirHTML( message=None ):
    listing = []
    if request.form["q"] != None: 
        listing = list_library(CONFIG_MAP['LIB_DIR'], CONFIG_MAP['DB_DIR'], urllib2.unquote(request.form["q"]))
    return render_template(
        'file_table.html', 
        listing=listing,
        message=message
    )

@app.route('/dir/delete', methods=['POST'])
def deleteDir(message=None ):
    if session.get("admin_auth_ok") == False:
        return "User not authorized"
    if request.method=='GET' and request.args.get("name") != None:  
        the_path = os.path.normpath(CONFIG_MAP['LIB_DIR'] + urllib2.unquote( request.args.get("name")) )
        if os.path.isfile( the_path ):
            return "Slected file was not a directory."
        else:
            shutil.rmtree( the_path )
            return "ok"
    else:
        return "Error"

@app.route('/dir/json', methods=['POST'])
def getDirJSON( message=None ):
    listing = []
    if request.form["q"] != None: 
        listing = list_library(CONFIG_MAP['LIB_DIR'], CONFIG_MAP['DB_DIR'], urllib2.unquote(request.form["q"]))
    return json.dumps( listing )

@app.route('/dir/download')
def getDirDownload( message=None ):
    print "Serving folder"
    the_zip = None
    if request.method=='GET' and request.args.get("q") != None: 
        path = os.path.normpath(CONFIG_MAP['LIB_DIR'] + "/" + urllib2.unquote(request.args.get("q")))
        print "Dir path: ", path
        #open zip file
        clean_folder(CONFIG_MAP['TEMP_DIR'])
        zip_path = CONFIG_MAP['TEMP_DIR'] + "/" + os.path.basename( path ) + ".zip" # create a location/ name for the zip file.
        print "Zip: ", zip_path
        the_zip = zipfile.ZipFile(zip_path, 'w') #make a zip file of this name
        #for f in os.listdir( path ):
        for root, dirs, files in os.walk(path):
            for file in files:
                print "loading file to zip: ", os.path.normpath(os.path.join(root, file))
                com_path = os.path.commonprefix([ os.path.normpath( path + "/junk" ), os.path.normpath(os.path.join(root, file)) ]) #the common part.
                new_file_name = os.path.join(root, file)[len(com_path):] #strip off front.
                the_zip.write(os.path.join(root, file), new_file_name) # (path to copy from, new file name)

        the_zip.close()
        return send_file(
            zip_path, 
            mimetype="application/octet-stream", 
            as_attachment=True)
    else:
        return "Error"


@app.route('/randomfile')
def getRandomFile(message=None ):
    # filename is the absolute path: 
    the_file = find_rand_file(CONFIG_MAP['LIB_DIR'])
    return send_file(the_file, mimetype="audio/mpeg", as_attachment=False) ## don't send as attachment, serve directly

@app.route('/random')
def getRandom(message=None ):
    the_file = find_rand_file(LIB_DIR)
    file_path = pathMinusLibrary(CONFIG_MAP['LIB_DIR'], the_file)
    return file_path

@app.route('/newdir')
def nakeDir(message=None ):
    try:
        if request.method=='GET' and request.args.get("name") != None and request.args.get("location") != None: 
            new_dir_path = os.path.normpath(CONFIG_MAP['LIB_DIR'] + "/" + request.args.get("location") + "/" + request.args.get("name"))
            os.mkdir(new_dir_path)
            return "Success"
        else:
            return "Error- name or location not set"
    except Exception, e:
        traceback.print_exc()
        print str(e)
        return "Error: " + str(e)
