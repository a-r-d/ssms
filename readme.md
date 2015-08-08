Super Simple Music Server
==========================



## SSMS

SSMS is a small music server written in Python. It lets you listen to music right from your browser using HTML5 media controls. Google chrome even has support for .mp3 and .mp4 playback so it is almost to point of being drag-and-drop as far as installation goes. You will however have to upload your library to you webserver/media server and configure the server. So it's not as simple as using pandora.

If you are like me you have your own private collection of .mp3 files that you have been accumulating since your teenage years and you are not willing to part with it, but uploading any of these onto many cloud services can be expensive. Amazon, Google Drive and Dropbox all charge serious monthly fees for a storing a large collection like I have. It is much cheaper and more fun to get a $5 a month VPS with 100 gb of capacity from ramnode or linode, upload your music there and then it expose it via some HTTP interface. You can use your VPS for plenty of other junk as well.



### Frontend code

The frontend code is pretty bad and needs to be re-written using a modern javascript framework. I started to refactor it and make it class based, and added all the deps under bower but it really needs to be cleaned up much much more.



### Backend code

The backend code is a little better after restructuring the routes but some libraries can be broken out further and organized a little bit better.



### Requirements

+ Linux OS (Mac OSX may work, not sure)

+ Python 2.6+

+ Python Modules:
    1. Flask +(dependencies for templates, ect- just use pip)
    2. Tornado
    3. sqlalchemy

+ Bower, which requires npm, which requires node. (npm install -g bower)

+ Cron- install a cron job to restart the server in case of crashing. 
    do something like: "20 * * * * /path/to/run.sh"

+ A bunch of music files! Put them wherever you point LIB_DIR to, by default it is '<project_path>/library' but you can change this in the admin panel easily.



### Installation

+ Install dependencies listed above.

+ Clone the repo to your server

+ install frontend deps: "cd ./ssms && bower install". If you don't have bower, it is a node application google it.

+ start it running:  
    ./run.sh > outputs.out &

+ set a different port if you like in server.py (default is 8888)

+ The DB file will be created on first run. Default passwords for user and admin are "password"

+ Go into the admin panel and point the library where you want it. Otherwise the app will read the 
    'library' dir from the base of the app. 

+ Save the admin settings and refresh the page. 


