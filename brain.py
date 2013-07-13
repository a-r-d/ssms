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
from settings import LOCAL_DEBUG, SECRET_KEY, DB_FILE_NAME, DB_LOCATION, SCHEMA_LOCATION, LOGS_LOCATION
from settings import LOGS_FILE_NAME, DEFAULT_LIBRARY_LOCATION, DEFAULT_BASE_DIR, DEFAULT_TEMP_LOCATION 
from settings import DEFAULT_USER_PASS, DEFAULT_ADMIN_PASS, OVERRIDE_PASSWORD
from backend.helpers import clean_folder
from backend.helpers import list_library
from backend.helpers import log
from backend.helpers import pathMinusLibrary # try to remove this.
from backend.helpers import find_rand_file
from backend.helpers import file_search
from backend.helpers import file_search_html
from backend.helpers import clean_folder

###########################################################
# get the dir name to be relative to.
BASE_DIR = DEFAULT_BASE_DIR
TEMP_DIR = BASE_DIR + DEFAULT_TEMP_LOCATION
LIB_DIR = DEFAULT_LIBRARY_LOCATION # note, this is absolute!
LOG_DIR = BASE_DIR + LOGS_LOCATION
LOG_FILE = LOG_DIR + LOGS_FILE_NAME
DB_DIR = BASE_DIR + DB_LOCATION
DATABASE = BASE_DIR + DB_LOCATION + DB_FILE_NAME
DB_SCHEMA = BASE_DIR + SCHEMA_LOCATION

# create app:
app = Flask(__name__)
app.secret_key = SECRET_KEY
UPLOAD_FOLDER = TEMP_DIR
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###########################################################
### DB Layer, and request before + after.
@app.before_request
def before_request():
    g.db = get_db()
    print "req path: " + request.path
    if request.path.startswith("/static") == False and request.path.startswith("/login") == False:
        #print "Non static path:"
        if 'user_auth_ok' in session:
            if session['user_auth_ok'] != True:
                return render_template('login_user.html', message="Please Log In!")
        else:
            return render_template('login_user.html',  message="Please Log In!")
    
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

## First run setup:
## make temp dirs, logs, ect - all on 'ignore' in the repo..:
dirs = [TEMP_DIR, LIB_DIR, LOG_DIR, DB_DIR]
for d in dirs:
    if not os.path.exists(d):
        print "Creating location: " + d
        os.makedirs(d)
        
if not os.path.exists(DATABASE):
    print "Creating database at: " + DATABASE
    init_db()
        
###########################################################
@app.route('/')
def home( message=None ):
    listing = list_library(LIB_DIR, DB_DIR)
    return render_template(
        'home.html', 
        listing=listing,
        message=message
        )

###
## Login stuff
###
   
@app.route('/login')
def loginFormUser( message=None ):
    return render_template(
        'login_user.html', 
        message=message
    )

@app.route('/admin')
def adminPanel( message=None ):
    if 'admin_auth_ok' in session and session["admin_auth_ok"] == True:
        #check to see if the passwords are set in settings or DB
        return render_template('admin.html', 
            message=message,
            LIB_PATH= os.path.normpath(LIB_DIR),
            user_pass_note="Password set in settings.py file",
            admin_pass_note="Password set in settings.py file",
            )
    else:
        return render_template('login_admin.html', message="You must authenticate first!")

# we will use ajax here.
@app.route('/admin/post', methods=['POST'])
def adminConfigPost( message=None ):
    if 'admin_auth_ok' in session and session["admin_auth_ok"] == True:
        # process the form:
        if "u_pass" in request.form:
            print "updating user pass"
        if "a_pass" in request.form:
            print "updating admin pass"
        if "lib_path" in request.form:
            if os.path.normpath( LIB_DIR ) != os.path.normpath( request.form["lib_path"] ):
                print "updating lib dir"

        return "Success"
    else:
        return "User not authenticated"
    

@app.route('/admin/auth', methods=['POST'])
def adminPanelAuth( message=None ):
    if 'password' in request.form:
        p_admin_test = request.form["password"]
        if p_admin_test == DEFAULT_ADMIN_PASS or p_admin_test == OVERRIDE_PASSWORD:
            session["admin_auth_ok"] = True
            return adminPanel()
        else:
            session["admin_auth_ok"] = False
            return render_template(
                'login_admin.html', 
                message="Password Incorrect!"
                )
    else:
        return render_template(
            'login_admin.html', 
            message="Password not set!"
            )

@app.route('/login/submit' , methods=['POST'])
def loginFormUserSubmit( message=None ):
    if request.method=='POST' and request.form["password"] != None:  
        p_word = request.form["password"]

        ### REWRITE WHEN DB IS WORKING!!
        if p_word == DEFAULT_USER_PASS or p_word == OVERRIDE_PASSWORD:
            session['user_auth_ok'] = True
            print "Authentication success!"
            return redirect("/", code=302)
        else:
            session['user_auth_ok'] = False
            print "Password was incorrect: " + p_word
            return render_template(
                'login_user.html', 
                message="Password is Incorrect!"
                )
    else: 
        return render_template(
            'login_user.html', 
            message="No Password set!"
            )

@app.route('/logout')
def logout( message=None ):
    #session.destroy()
    return render_template(
        'login_user.html', 
        message=message
        )

###
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

@app.route('/newdir')
def nakeDir(message=None ):
    try:
        if request.method=='GET' and request.args.get("name") != None and request.args.get("location") != None: 
            new_dir_path = os.path.normpath( LIB_DIR + "/" + request.args.get("location") + "/" + request.args.get("name"))
            os.mkdir(new_dir_path)
            return "Success"
        else:
            return "Error- name or location not set"
    except Exception, e:
        traceback.print_exc()
        print str(e)
        return "Error: " + str(e)

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
        traceback.print_exc()
        print str(e)
        return "error: " + str(e)
        
############################################################################
# end routes
############################################################################
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['mp3', 'm4a', 'mp3', 'ogg', 'wma', 'mov'])
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
