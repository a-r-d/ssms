#-*- coding: utf-8 -*-
import os
import shutil
import random
from datetime import datetime
import traceback

"""
Do some logging:
"""
def log( some_string ):
    from brain import LOG_DIR
    try:
        dt = datetime.now()
        f = open(LOG_DIR + "/out.log", 'a')
        f.write( str( dt ) + ": " + some_string + "\n" )
        f.close()
        print some_string
    except Exception, e:
        traceback.print_exc()
        print str(e)
        
"""
Cleans out the current update folder:
"""
def clean_folder( path ):
    folder = path
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            #if os.path.isfile(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree( file_path )
            else:
                os.unlink( file_path )
        except Exception, e:
            print e
            log( "clean_folder fail- " + str(e) )
            
            
"""
Get library listing:

"""
def list_library(lib_dir, db_dir, some_path=None):
    listing = []
    skip_list = ["..","."]
    target_dir = lib_dir
    if some_path != None:
        # lib dir has no trailing slash, some_path has a trailing slash.
        target_dir = lib_dir + "/" + some_path
    try:
        #print 'Listing target_dir:', target_dir
        # if you pass in a unicode string, os.listdir returns unicode results...
        for a_file in os.listdir( target_dir.decode('utf-8') ):
            file_path = os.path.join( target_dir + u"/" , a_file )
            try:
                if os.path.basename(file_path) not in skip_list and ( test_ext( file_path ) or os.path.isdir( file_path )):
                    if os.path.isdir( file_path ):
                        listing.append( file_path )
                    else:
                        listing.append( file_path )
            except Exception, e:
                print "list_library inner loop: ", str(e)
                continue
    except Exception, e:
        print "list_library: ", str(e)
        log( "list_library: " + str(e) )
    
    ##print listing
    listing.sort()
    made_objects = []
    for l in listing:
        made_objects.append( renderPath(lib_dir, l) )
        
    return made_objects

"""
Searches for a file by matching name:
    #mode must be either "full_path" or "name"
"""
def file_search(LIB_DIR, search_string, mode="full_path"):
    matches = []
    # if you pass in a unicode string, os.walk returns unicode results...
    for root, dirs, files in os.walk( LIB_DIR ): ## tried LIB_DIR.decode('utf-8') , didnt work on server.
        for file in files:
            try:
                if mode == "full_path":
                    to_search = pathMinusLibrary(LIB_DIR, os.path.normpath(os.path.join( root, file )))
                    if to_search.lower().find( search_string.lower() ) != -1 and test_ext( file ):
                        matches.append( os.path.join( root, file))
                else:
                    if file.lower().find( search_string.lower() ) != -1 and test_ext( file ):
                        matches.append( os.path.join( root, file))
            except Exception, e:
                log("Error on search: " + str(e) + " for file:" + file)
                continue
    #sort it:
    matches.sort()
    return matches 

def file_search_html(LIB_DIR, search_string):
    matches = file_search(LIB_DIR, search_string)

    file_dict_for_template = []
    for match in matches:
        file_dict_for_template.append(renderPath(LIB_DIR, match ))

    return file_dict_for_template
    
    
"""
Walks on the LIB_DIR to get a random file.
"""
def find_rand_file(LIB_DIR):
    the_count = 0
    for root, dirs, files in os.walk(LIB_DIR):
        for file in files:
            the_count += 1
            
    the_stopper = int(random.random() * the_count) # conv to int
    print "Stopped on: ", the_stopper, " out of: ", the_count
    
    i = 0
    the_file = None
    for root, dirs, files in os.walk(LIB_DIR):
        found = False
        for file in files:
            if i >= the_stopper and os.path.isfile(os.path.join( root, file )) and test_ext(file):
                the_file = os.path.normpath( os.path.join( root, file))
                found = True
                break
            i += 1
        if found:
            break
    
    print "Random: ", the_file
    return the_file

def test_ext( filename ):
    filter = [".mp3", ".m4a", ".mp4", '.ogg']
    for ext in filter:
        if filename.lower().find( ext.lower() ) != -1:
            return True
    return False
    
########################################################################################
### Don't expose these outside of file,
########################################################################################
def pathMinusLibrary( lib_dir, path_dir):
    ## why do this? we dont want to serve whole to the world!
    com_path = os.path.commonprefix([
        os.path.normpath( lib_dir ), 
        os.path.normpath( path_dir )
        ]) 
    #print "common path: ", com_path
    after_lib_only = path_dir[len(com_path):]
    #print "after_lib_only: ", after_lib_only
    return after_lib_only
    
def isValidExtension( extension ):
    valid = [".mp3", ".mp4", ".ogg", ".m4a"]
    if extension in valid:
        return True
    return False
    
# returns a dict of what I want my files to look like in my templates. 
def renderPath( lib_dir, file_path ):
    if os.path.isdir( file_path ):
        return {
            "name": os.path.basename( file_path ),
            'path': file_path,
            'safePath': pathMinusLibrary( lib_dir, file_path),
            'size': os.path.getsize( file_path ),
            'sizeStr': "%s kb" % str(os.path.getsize( file_path ) / 1000),
            'isDir': True,
            'isPlayable': isValidExtension( os.path.splitext( file_path )[1] ),
            'extension': os.path.splitext( file_path )[1]
        }
    else:
        return {
            'name': os.path.basename( file_path ),
            'path': file_path,
            'safePath': pathMinusLibrary( lib_dir, file_path),
            'size': os.path.getsize( file_path ),
            'sizeStr': "%s kb" % str(os.path.getsize( file_path ) / 1000),
            'isDir': False,
            'isPlayable': isValidExtension( os.path.splitext( file_path )[1] ),
            'extension': os.path.splitext( file_path )[1]
        }

"""
Cleans out a folder:
"""
def clean_folder( path ):
    folder = path
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            #if os.path.isfile(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree( file_path )
            else:
                os.unlink( file_path )
        except Exception, e:
            print e
            log( "clean_folder fail- " + str(e) )

    
    
    
    
