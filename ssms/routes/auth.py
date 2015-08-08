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
            LIB_PATH= os.path.normpath(CONFIG_MAP['LIB_DIR']),
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
            entry = g.db.query(UserPrefs).filter_by(key='user_pass').first() 
            print entry
            entry.val = request.form["u_pass"]
        if "a_pass" in request.form:
            print "updating admin pass"
            entry = g.db.query(UserPrefs).filter_by(key='admin_pass').first() 
            print entry
            entry.val = request.form["a_pass"]
        if "lib_path" in request.form:
            if os.path.normpath( LIB_DIR ) != os.path.normpath( request.form["lib_path"] ):
                print "updating lib dir"
                entry = g.db.query(UserPrefs).filter_by(key='lib_dir').first() 
                print entry
                entry.val = request.form["lib_path"]

        # commit after all changes take place
        g.db.commit()

        return "Success"
    else:
        return "User not authenticated"
    

@app.route('/admin/auth', methods=['POST'])
def adminPanelAuth( message=None ):
    if 'password' in request.form:
        p_admin_test = request.form["password"]
        db_password = None
        try:
            entry = g.db.query(UserPrefs).filter_by(key='admin_pass').first() 
            if entry:
                db_password = entry.val
        except Exception, e:
            log(str(e))
            print "adminPanelAuth db fail- ", str(e)
        ## test against the DB first:
        if db_password != None:
            if p_admin_test == db_password or p_admin_test == CONFIG_MAP['OVERRIDE_PASSWORD']:
                session["admin_auth_ok"] = True
                return adminPanel()
            else:
                session["admin_auth_ok"] = False
                return render_template(
                    'login_admin.html', 
                    message="Password Incorrect!"
                )
        else:
            if p_admin_test == DEFAULT_ADMIN_PASS or p_admin_test == CONFIG_MAP['OVERRIDE_PASSWORD']:
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
        db_password = None
        try:
            entry = g.db.query(UserPrefs).filter_by(key='user_pass').first() 
            if entry:
                db_password = entry.val
        except Exception, e:
            log(str(e))
            print "loginFormUserSubmit db fail- ", str(e)

        ## test against the DB first:
        if db_password != None:
            if p_word == db_password or p_word == CONFIG_MAP['OVERRIDE_PASSWORD']:
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
            if p_word == DEFAULT_USER_PASS or p_word == CONFIG_MAP['OVERRIDE_PASSWORD']:
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

@app.route('/logout/admin')
def logoutAdmin( message=None ):
    #don't bother with destroying session.
    session["admin_auth_ok"] = False
    return redirect("/")

@app.route('/logout')
def logout( message=None ):
    #don't bother with destroying session.
    session['user_auth_ok'] = False
    session["admin_auth_ok"] = False
    return render_template(
        'login_user.html', 
        message=message
    )
