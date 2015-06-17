from datetime import datetime
from ssms.settings import CONFIG_MAP

"""
Do some logging:
"""
def log( some_string ):
    try:
        dt = datetime.now()
        f = open(CONFIG_MAP['LOG_DIR'] + "/out.log", 'a')
        f.write( str( dt ) + ": " + some_string + "\n" )
        f.close()
        print some_string
    except Exception, e:
        traceback.print_exc()
        print str(e)
