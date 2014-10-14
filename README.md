ink-bottle
==========

A minimal skeleton for doing Bottle apps in a structured fashion (targeting Python 2.7 or above), meant as reference code for training sessions.

Should be usable out of the box (even if it only displays one view).

## Filesystem Layout

<pre>
+-- app.py                # entry point
+-- etc
|    +-- default.json     # main configuration file
+-- api
|    +-- [model].py       # RESTful routes for each model
+-- routes 
|    +-- [kind].py        # all other routes (static, actions, etc.)
+-- controllers
|    +-- [behavior].py    # controllers used by routes
+-- lib
|    +-- bottle.py        # more bang than Flask
|    +-- peewee.py        # almost as nice as the Django ORM
|    +-- config.py        # loads up the JSON file 
|    +-- utils            # my little bag of tricks
|    |    +-- core.py
|    |    +-- urlkit.py
|    |    +-- stringkit.py
|    |    +-- datekit.py
|    +-- [dependencies]   # Include ALL the dependencies locally
+-- models
|    +-- db.py            # Base models and database setup
|    +-- [store].py       # Other data stores (Redis, etc.)
+-- static                # Static assets (HTML and sundry)
+-- views
     +-- layout.tpl       # Base layout for templates
     +-- [group]          # Partials for each entity/screen
</pre>


## Running

    make serve


## Note

Don't forget to do `git submodule update --init` when checking out the source.
