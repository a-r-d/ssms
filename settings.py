#-*- coding: utf-8 -*-
import os
import socket

def configure():
    ###########################################################
    # get the dir name to be relative to.

    # you can move the base directory somewhere else if you wish, but the whole idea is for easy installation!
    DEFAULT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    DEFAULT_LIBRARY_LOCATION = DEFAULT_BASE_DIR + "/library" # supply an absolute path for this.
    DEFAULT_LIBRARY_LOCATION = "D:/music"

    # you should not have to change this, it is mostly settable in the DB.  
    DEFAULT_TEMP_LOCATION = "/temp"         # relative to base dir set above, defaults to app base dir.
    LOGS_LOCATION = "/logs"                 # relative to base dir set above, defaults to app base dir.
    LOGS_FILE_NAME = "/out.log"             # relative to base dir set above, defaults to app base dir.
    DB_LOCATION =  "/db"                    # relative to base dir set above, defaults to app base dir.
    DB_FILE_NAME = "/main.db"               # relative to base dir set above, defaults to app base dir. 
    SCHEMA_LOCATION = "/db/schema.sql"      # relative to base dir set above, defaults to app base dir.


    BASE_DIR = DEFAULT_BASE_DIR
    TEMP_DIR = BASE_DIR + DEFAULT_TEMP_LOCATION
    LIB_DIR = DEFAULT_LIBRARY_LOCATION # note, this is absolute!
    LOG_DIR = BASE_DIR + LOGS_LOCATION
    LOG_FILE = LOG_DIR + LOGS_FILE_NAME
    DB_DIR = BASE_DIR + DB_LOCATION
    DATABASE = BASE_DIR + DB_LOCATION + DB_FILE_NAME
    DB_SCHEMA = BASE_DIR + SCHEMA_LOCATION

    LOCAL_DEBUG = False
    PORT = 8888
    HOST = '0.0.0.0'

    # special debug hosts
    if socket.gethostname() in ["waffles", "ares", "ard"]:
        LOCAL_DEBUG = True
    elif socket.gethostname() == "web335.webfaction.com":
        LOCAL_DEBUG = True
        PORT = 17944

    return {
        'BASE_DIR': BASE_DIR,
        'TEMP_DIR': TEMP_DIR,
        'LIB_DIR': LIB_DIR,
        'LOG_DIR': LOG_DIR,
        'LOG_FILE': LOG_FILE,
        'DB_DIR': DB_DIR,
        'DATABASE': DB_DIR,
        'DB_SCHEMA': DB_SCHEMA,
        'LOCAL_DEBUG': LOCAL_DEBUG,
        'PORT': PORT,
        'INIT_DIRS': [
            TEMP_DIR,
            LIB_DIR,
            LOG_DIR,
            DB_DIR
        ]
    }


#######################################
### Exposed directly
#######################################

LOCAL_DEBUG = True
SECRET_KEY = 'ifjdsfJKLFDJKLFHDSKutgh98wrg983103j24hrtj' #change this when you deploy!

## the default passwords are really just temporary in case the DB is not in use
DEFAULT_USER_PASS = "password"          # if set in DB, it is overriden
DEFAULT_ADMIN_PASS = "password"         # ditto to the above
OVERRIDE_PASSWORD = "incaseyouforget"   #in case you forget the password set in the DB. 
CONFIG_MAP = configure()