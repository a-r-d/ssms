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

######################### playlist #############################################
@app.route("/playlist/new")
def mkPlaylist(message=None):
    if request.method=='GET' and request.args.get("name") != None: 
        name = request.args.get("name")
        new_pl = Playlist(name)
        g.db.add( new_pl )
        pl_list = g.db.query(Playlist).all()
        g.db.commit()
        return render_template(
            'playlists_list.html', 
            playlists=pl_list,
            message=message
        )
    else:
        return "fail"

@app.route("/playlist/del")
def delPlaylist(message=None):
    if request.method=='GET' and request.args.get("id") != None: 
        id = request.args.get("id")

        entry = g.db.query(Playlist).filter_by(id=id).first() 
        g.db.delete( entry )
        g.db.commit()

        return render_template(
            'playlists_list.html', 
            message=message
        )
    else:
        return "fail"

@app.route("/playlist/menu")
def getPlaylistAddMenu(message=None):
    playlist = g.db.query(Playlist).all()
    return render_template(
        'playlists_selection.html', 
        playlists=playlist,
        message=message
    )

@app.route("/playlist/item/add")
def addPlaylistItem(message=None):
    if request.method=='GET' and \
        request.args.get("id") != None and \
        request.args.get("path") != None and \
        request.args.get("list_order") != None: 

        id = request.args.get("id")
        path = request.args.get("path")
        list_order = request.args.get("list_order")

        new_pl_item = PlaylistItem(id, path, list_order)
        g.db.add( new_pl_item )
        g.db.commit()

        return "ok"
    else:
        return "fail"

@app.route("/playlist/item/del")
def delPlaylistItem(message=None):
    if request.method=='GET' and request.args.get("id") != None and request.args.get("playlist_id") != None: 
        id = request.args.get("id")
        playlist_id = request.args.get("id")
        entry = g.db.query(PlaylistItem).filter_by(id=id).first() 
        g.db.delete( entry )
        g.db.commit()
        # get the new list
        playlist = g.db.query(Playlist).filter_by(id=playlist_id).first() 
        playlist_items = g.db.query(PlaylistItem).filter_by(playlist_id=playlist.id)
        return render_template(
            "playlist_item_list.html",
            playlist = playlist,
            playlist_items = playlist_items, 
            message=message
        )
    else:
        return "fail"

# pass playlist ID to edit.
@app.route("/playlist/edit/<id>")
def editPlaylistByID(id, message=None):
    playlist = g.db.query(Playlist).filter_by(id=id).first() 
    if playlist == None:
        return "Empty"
    playlist_items = g.db.query(PlaylistItem).filter_by(playlist_id=playlist.id)
    return render_template(
            "playlist_item_list.html",
            playlist = playlist,
            playlist_items = playlist_items, 
            message=message
        )

# pass playlist ID to load
@app.route("/playlist/load/<id>")
def loadPlaylistByID(id, message=None):
    playlist = g.db.query(Bookmark).filter_by(id=id).first() 
    playlist_items = g.db.query(PlaylistItem).filter_by(playlist_id=playlist.id)
    return render_template(
            playlist = playlist,
            playlist_items = playlist_items, 
            message=message
        )