Super Simple Music Server
==========================



##*SSMS*

SSMS is a small music server written in Python. It lets you listen to music right from your browser using HTML5. Google chrome even has support for .mp3 and .mp4 playback so it is almost to point of being drag-and-drop as far as installation goes. You will however have to upload your library to you webserver/ media server/ open ports on your firewall. So its not as simple as using pandora. I have my own music collection I have been working on for years though, and would like to keep hold of it!



##*Requirements*

+ Python 2.6+

+ Non-Standard Python Modules:
    1. Flask +(dependencies for templates, ect- just use pip)
    2. Tornado
    3. sqlalchemy

+ Cron- install a cron job to restart the server in case of crashing. 
    do something like: "20 * * * * /path/to/run.sh"

+ A bunch of music files! Put them wherever you point LIB_DIR to, by default it is
    [project_path]/library




##*Installation*

+ Install dependencies listed above.

+ Drop the files in the repo somehere on your server

+ start it running:  
    ./run.sh > outputs.out &

+ set a different port if you like in server.py (default is 8888)

+ The DB file will be created on first run. Default passwords for user and admin are "password"

+ Go into the admin panel and point the library where you want it. Otherwise the app will read the 
    'library' dir from the base of the app. 

+ Save the admin settings and refresh the page. 
+



##*why!?*

I wanted: 
+ 1. Browser playback of my media files from anywhere. 
+ 2. Good support for mobile devices. 
+ 3. On the fly file conversion (e.g. .mp3 to .ogg for firefox!)
+ 4. The files to appear like a NAS on the network (optional).
+ 5. An easy way to organize the files you upload. 
+ 6. Password protection on the server. 

