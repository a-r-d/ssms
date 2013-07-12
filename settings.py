import os

LOCAL_DEBUG = False

SECRET_KEY = 'ifjdsfJKLFDJKLFHDSKutgh98wrg983103j24hrtj' #change this when you deploy!

DEFAULT_USER_PASS = "password" 			# if set in DB, it is overriden
DEFAULT_ADMIN_PASS = "password" 		# ditto to the above
OVERRIDE_PASSWORD = "incaseyouforget" 	#in case you forget the password set in the DB. 



# you can move the base directory somewhere else if you wish, but the whole idea is for easy installation!
DEFAULT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_LIBRARY_LOCATION = DEFAULT_BASE_DIR + "/library" # supply an absolute path for this.

# you should not have to change this, it is mostly settable in the DB.  
DEFAULT_TEMP_LOCATION = "/temp"			# relative to base dir set above, defaults to app base dir.
LOGS_LOCATION = "/logs"  				# relative to base dir set above, defaults to app base dir.
LOGS_FILE_NAME = "/out.log" 			# relative to base dir set above, defaults to app base dir.
DB_LOCATION =  "/db"					# relative to base dir set above, defaults to app base dir.
DB_FILE_NAME = "/main.db"				# relative to base dir set above, defaults to app base dir. 
SCHEMA_LOCATION = "/db/schema.sql" 		# relative to base dir set above, defaults to app base dir.

