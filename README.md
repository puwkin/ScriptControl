This is still a work in progress so use at your own risk. 

If you do find any bugs please report them to **[eddy.hintze+bugs@gmail.com](mailto:eddy.hintze+bugs@gmail.com)** with subject: **ScriptControl**

The ScriptControl project is used to control multiple python scripts remotely. This is done via an api created using *Flask*. See **API** below for list of commands.

Use this web interface to control this project: [Control-Interface](https://github.com/xtream1101/control-interface)


Dependencies
------------

  * Python 3.x
  * sqlite3
  * Flask
  * Flask-Cors
  

API
---
Returns a list of scripts and their info

    /script/list
    
Rescans the scripts dir and adds new scripts to the list

    /script/list/update

All calls below will return a JSON object with:

  - **output** which contains the response text
  - **return** which will return a bool with the success of the command sent
  
Enables the script to be run

    /script/<name>/enable
    
Disables the script from running

    /script/<name>/disable

Runs the script if enabled

    /script/<name>/run
    
Returns the current output of the script

    /script/<name>/output/live
    
Stops the script during the current call where `if not self._running: break` is found in the loop

    /script/<name>/stop


Usage
-----

1. Install the dependencies listed above.

2. Use loop.py as a template on how to create your own
