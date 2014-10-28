import os
import flask
from flask.ext.cors import CORS
import json
import threading
import history
import script
import log

app = flask.Flask(__name__)
cors = CORS(app, resources=r'/api/*', headers='Content-Type')


@app.route('/')
def index():
    return "Home Page"


@app.route('/api/script/list', methods=['GET'])
def get_script_list():
    """
    DONE
    Return a list of the scripts
    """
    #List all unused scripts that are in the ./scripts/ dir
    list_all = []
    for key in script_list:
        list_all_info = {
            'name': key,
            'uptime': script_list[key].get_uptime(),
            'last_run': script_list[key].get_last_run(),
            'running': script_list[key].is_running(),
            'enabled': script_list[key].is_enabled(),
            'trigger': script_list[key].get_trigger_type(),
            'trigger_setting': script_list[key].get_trigger_settings()
        }
        list_all.append(list_all_info)
    return flask.jsonify({'all': list_all, 'return': True})


@app.route('/api/script/list/update', methods=['GET'])
def update_script_list():
    #rescan scripts dir
    add_scripts()
    return flask.jsonify({'output': 'List Updated', 'return': True})


@app.route('/api/script/<script_name>/run', methods=['GET'])
def script_run(script_name):
    """
    DONE
    Adds script to the scriptList and creates an object
    """
    output, return_val = script_list[script_name].run()
    log_.warning('Run ('+script_name+'): '+str(return_val)+' - '+output)
    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/api/script/<script_name>/enable', methods=['GET'])
def script_enable(script_name):
    """
    DONE
    Enables script if configured
    """
    output, return_val = script_list[script_name].set_enabled()
    log_.warning('Enable ('+script_name+'): '+str(return_val)+' - '+output)
    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/api/script/<script_name>/disable', methods=['GET'])
def script_disable(script_name):
    """
    DONE
    Disables script
    """
    output, return_val = script_list[script_name].set_disabled()
    log_.warning('Disable ('+script_name+'): '+str(return_val)+' - '+output)
    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/api/script/<script_name>/stop', methods=['GET'])
def script_stop(script_name):
    """
    DONE
    Stops script
    """
    output, return_val = script_list[script_name].stop()
    log_.warning('Disable ('+script_name+'): '+str(return_val)+' - '+output)
    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/api/script/<script_name>/setting/<string:setting>/<int:value>', methods=['GET'])
def script_set_trigger(script_name, setting, value):
    """
    DONE
    Set script trigger settings
    """
    output, return_val = script_list[script_name].set_trigger_setting(setting, value)
    log_.warning('Set Trigger ('+script_name+'): '+str(return_val)+' - '+output)
    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/api/script/<script_name>/output/hist/<string:amount>', methods=['GET'])
@app.route('/api/script/<script_name>/output/hist/<string:amount>/<int:limit>', methods=['GET'])
def get_output_history(script_name, amount, limit=1):
    """
    DONE
    Get the history of a scripts output
    all: gets all output sorted by newest first
    last: gets latest output, if a limit is passed it will get the last n outputs
    """
    return_val = True
    if amount.lower() == "all":
        output = hist.get_all(script_name)
    elif amount.lower() == "last":
        output = hist.get_last(script_name, limit)
    else:
        output = "Invalid call"
        return_val = False
 
    log_.warning('Output History ('+script_name+'): '+str(return_val)+' - '+output)
    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/api/script/<script_name>/output/live', methods=['GET'])
def get_output_live(script_name):
    """
    DONE
    Get the live output
    """
    output, return_val = script_list[script_name].get_output()
    log_.warning('Output Live ('+script_name+'): '+str(return_val)+' - '+str(output))
    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/api/script/<script_name>/next_run', methods=['GET'])
def get_next_run(script_name):
    output, return_val = script_list[script_name].get_next_run()
    return flask.jsonify({'output': output, 'return': return_val})


def save_data():
    """
    Saves data about the script_list every 5 seconds
    """
    save_list = {}
    for key in script_list:
        save_list[key] = {
            'trigger_settings': script_list[key].get_trigger_settings(),
            'enabled': script_list[key].is_enabled(),
            'next_run': script_list[key].get_next_run()
        }
    with open('data.json', 'w') as outfile:
        json.dump(save_list, outfile)
    print("save data")
    threading.Timer(5, save_data).start()

def load_data():
    with open('data.json') as data_file:
        data = json.load(data_file)
    return data

def add_scripts():
    saved = load_data()
    for each_file in os.listdir("./scripts/"):
        file_name = os.path.splitext(os.path.basename(each_file))
        if file_name[1] == ".py" \
                and each_file != "__init__.py" \
                and each_file != "template.py":
            script_name = file_name[0]
            if script_name not in script_list.keys():
                script_list[script_name] = script.Script(script_name)
                if script_name in saved: #then read in old values
                    #add back any settings
                    if script_list[script_name].get_trigger_type() != 'call':
                        saved_setting = saved[script_name]['trigger_settings']
                        for setting in saved_setting:
                            script_list[script_name].set_trigger_setting(setting, saved_setting[setting])
                    #set to last enabled state
                    if saved[script_name]['enabled']:
                        script_list[script_name].set_enabled()


if __name__ == '__main__':
    #set up general log file
    log_ = log.Log('./_log.db')
    #set up script history log
    hist = history.History('./scripts/_history.db')
    #dict to store scripts data
    script_list = {}
    add_scripts()
    save_data()
    log_.error("Main script started")
    app.run(port=5001, host='0.0.0.0', debug=False)
