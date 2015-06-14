#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

import sqlite3

from helpers import log

DB_LOC = "../db/main.db" #the default, for testing.
ENGINE = None

def openDB( db_loc ):
	try:
		engine = create_engine("sqlite:///" + db_loc, echo=True)
		print engine.execute("select 1").scalar()
		global ENGINE
		ENGINE = engine
		return engine
	except Exception, e:
		print "Exceptiion opening DB cxn: ", str(e)
		print "Attempted to open DB @:", db_loc
		log(str(e))
		return None

def getSession( db_loc ):
	try:
		engine = None
		if ENGINE != None:
			engine = ENGINE
		else:
			engine = openDB( db_loc )
		Session = sessionmaker()
		Session.configure(bind=engine)
		this_session = Session()
		return this_session
	except Exception, e:
		print "Exceptiion getting a session: ", str(e)
		log(str(e))
		return None

##################################################################
Base = declarative_base()

class UserPrefs(Base):
	__tablename__ = 'user_prefs'

	key = Column(String, primary_key=True)
	val = Column(String)

	def __init__(self, key, val):
		self.key = key
		self.val = val

	def __repr__(self):
		return "<UserPrefs('%s','%s'')>" % (self.key, self.val)

def testUserPrefs():
	print "\nTesting user_prefs (UserPrefs):\n"
	Session = sessionmaker()
	Session.configure(bind=ENGINE)
	this_session = Session()

	#show prefs:
	res = this_session.query(UserPrefs).order_by(UserPrefs.key)
	for rec in res:
		print rec

	this_session.commit()

##################################################################

class Playlist( Base ):
	__tablename__ = "playlist"

	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "<UserPrefs('%s','%s'')>" % (str(self.id), self.name)

def testPlaylist():
	print "\nTesting playlist (Playlist):\n"
	Session = sessionmaker()
	Session.configure(bind=ENGINE)
	this_session = Session()

	#show prefs:
	res = this_session.query(Playlist).order_by(Playlist.id)
	for rec in res:
		print rec

	this_session.commit()

##################################################################

class PlaylistItem( Base ):
	__tablename__ = "playlist_item"

	id = Column(Integer, primary_key=True)
	playlist_id = Column(Integer)
	path = Column(String)
	list_order = Column(Integer)

	def __init__(self, playlist_id, path, list_order):
		self.playlist_id = playlist_id
		self.path = path
		self.list_order = list_order

	def __repr__(self):
		return "<UserPrefs('%s','%s','%s','%s')>" % (str(self.id), str(self.playlist_id), self.path, str(self.list_order))


def testPlaylistItem():
	print "\nTesting playlist item (Playlist):\n"
	Session = sessionmaker()
	Session.configure(bind=ENGINE)
	this_session = Session()

	#show prefs:
	res = this_session.query(PlaylistItem).order_by(PlaylistItem.id)
	for rec in res:
		print rec

	this_session.commit()


####################################################################

## bookmark loads and begins to play a given directory.
class Bookmark( Base ):
	__tablename__ = "bookmark"

	id = Column(Integer, primary_key=True)
	name = Column(String)
	path = Column(String)
	list_order = Column(Integer)

	def __init__(self, name, path, list_order):
		self.name = name
		self.path = path
		self.list_order = list_order

	def __repr__(self):
		return "<UserPrefs('%s','%s','%s','%s')>" % (str(self.id), self.name, self.path, str(self.list_order))


def testBookmark():
	print "\nTesting bookmark (Bookmark):\n"
	Session = sessionmaker()
	Session.configure(bind=ENGINE)
	this_session = Session()

	#show prefs:
	res = this_session.query(Bookmark).order_by(Bookmark.id)
	for rec in res:
		print rec

	this_session.commit()


##################################################################
if __name__ == '__main__':
    print "\nTest open DB + query: \n"
    openDB( DB_LOC )
    print "\nTest get session:\n"
    s = getSession( DB_LOC )
    print "\nTest close session:\n"
    s.commit()
    print "\nTest read entities: \n"
    testUserPrefs()
    testPlaylist()
    testPlaylistItem()
    testBookmark()
