#-*- coding: utf-8 -*-
# flask app:
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for, redirect
from flask import Response
from flask import send_file
from flask import g
from werkzeug import secure_filename

# built in:
from datetime import datetime
import os 
import socket # to get hostname
import shutil # to copy/del folders.
import distutils.core #to copy tree silently
import subprocess # to restart server.
import time # to wait for server.
import json
import random
import urllib2
import zipfile
import traceback

#external libs:
import sqlite3

# internal junk
from backend.helpers import clean_folder
from backend.helpers import list_library
from backend.helpers import log
from backend.helpers import pathMinusLibrary
from backend.helpers import find_rand_file
from backend.helpers import file_search
from backend.helpers import file_search_html
from backend.helpers import clean_folder

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

UPLOAD_FOLDER = TEMP_DIR
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        path = os.path.normpath( LIB_DIR + urllib2.unquote( request.args.get("q")) )
        #print "Serving file: ", path
        return send_file(path, mimetype="audio/mpeg", as_attachment=False) ## don't send as attachment, serve directly
    else:
        return "Error"

@app.route('/file/download')
def getFileDownload(message=None ):
    if request.method=='GET' and request.args.get("q") != None:  
        the_path = os.path.normpath( LIB_DIR + urllib2.unquote( request.args.get("q")) )
        return send_file(the_path, mimetype="audio/mpeg", as_attachment=True)
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

@app.route('/dir/download')
def getDirDownload( message=None ):
    print "Serving folder"
    the_zip = None
    if request.method=='GET' and request.args.get("q") != None: 
        path = os.path.normpath( LIB_DIR + "/" + request.args.get("q"))
        print "Dir path: ", path
        #open zip file
        clean_folder( TEMP_DIR )
        zip_path = TEMP_DIR + "/" + os.path.basename( path ) + ".zip" # create a location/ name for the zip file.
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


@app.route('/search')
def searchHTML( message=None ):
    res = []
    if request.method=='GET' and request.args.get("q") != None: 
        res = file_search_html(LIB_DIR, request.args.get("q"))
    return render_template(
        'file_table.html', 
        listing=res,
        message=message
        )

@app.route('/search/json')
def search( message=None ):
    res = []
    if request.method=='GET' and request.args.get("q") != None: 
        res = file_search(LIB_DIR, request.args.get("q"))
    return json.dumps( res )

@app.route('/admin')
def adminPanel():
    return render_template(
        'admin.html', 
        message=message
        )
        
@app.route('/randomfile')
def getRandomFile(message=None ):
    # filename is the absolute path: 
    the_file = find_rand_file(LIB_DIR)
    return send_file(the_file, mimetype="audio/mpeg", as_attachment=False) ## don't send as attachment, serve directly

@app.route('/random')
def getRandom(message=None ):
    the_file = find_rand_file(LIB_DIR)
    file_path = pathMinusLibrary(LIB_DIR, the_file)
    return file_path

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


ALLOWED_EXTENSIONS = set(['mp3', 'm4a', 'mp3', 'ogg', 'wma', 'mov'])

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
                upload_to = os.path.normpath( LIB_DIR + "/" + loc)
                print "upload to: " + upload_to
                file.save(os.path.join(upload_to, filename))
                listing = list_library(LIB_DIR, DB_DIR, loc)
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
        #traceback.print_exc()
        print str(e)
        return "error: " + str(e)

    
        
############################################################################
# end routes
############################################################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
#############################################################
if __name__ == '__main__':
    print "starting in: " + BASE_DIR
    if socket.gethostname() == "waffles":
        LOCAL_DEBUG = True
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')
