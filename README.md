# busapp

Written in some 48 hours during the Code 66 Albuquerque Hackathon 2012.

## Credits

 * Samat Jain - samat@samat.org - http://samat.org/
 * Zerek Welz - zerek@zerekwelz.com
 * Chris Hughes - chris@speedycomputing.com

## Installation

### Dependencies

* MySQL
* memcached
* Web server for serving static files, optionally WSGI
* A bunch of Python dependencies I don't remember
* A bunch of PHP dependencies I don't remember either
* CoffeeScript and probably another set of nodejs dependencies I don't remember either

### Database server

1. Create a database "code66".
2. Import schema into the database:

<code>
mysql -u root code66 < mysql.schema
</code>

3. Import stops information (you only need to do this when stops have been changed/updated):

<code>
python mysql-import-stops.py
</code>

### Daemons

1. In a screen session or similar (e.g. tmux), run:

<code>
python mysql-import.py
</code>

2. Either configure to run in a WSGI container, or also in screen, run:

<code>
python memcache-web-server.py
</code>

### Web client

1. Decide where you're hosting the static resources. Preferably on it's own domain. E.g. example.com.
2. Around line 32 in fetchBusLocations in script.coffee, change AJAX JSON request to point to realtime data server (step 2 of daemons).
3. Around line 122 in updateUs in script.coffee, change AJAX JSON request to point to stops info API (if you picked example.com as your site root, then this URL would be http://example.com/stops.php)
4. Recompile JavaScript by typing `make`.
5. Go to your site (e.g. http://example.com/) and watch everything work!
