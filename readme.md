Super Simple Music Server
==========================

*SSMS*

SSMS is a small music server written in Python. It lets you listen to music right from your browser using HTML5. Google chrome even has support for .mp3 and .mp4 playback so it is almost to point of being drag-and-drop. 


*Requirements*

a) Python 2.6+

b) Non-Standard Python Modules:
    1. Flask +(dependencies for templates, ect- just use pip)
    2. Tornado

c) Cron- install a cron job to restart the server in case of crashing. 

d) A bunch of music files! Put them wherever you point LIB_DIR to, by default it is
    [project_path]/library




*why!?*

I wanted: 
1. Browser playback of my media files from anywhere. 
2. Good support for mobile devices. 
3. On the fly file conversion (e.g. .mp3 to .ogg for firefox!)
4. The files to appear like a NAS on the network (optional).
5. An easy way to organize the files you upload. 
6. Password protection on the server. 

