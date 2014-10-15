import os
import flask
import history
import script
import log
from crossdomain import crossdomain

app = flask.Flask(__name__)


@app.route('/')
def index():
    return "Home Page"


@app.route('/script/list', methods=['GET'])
@crossdomain(origin='*')
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
            'running': script_list[key].is_running(),
            'enabled': script_list[key].is_enabled(),
            'trigger': script_list[key].get_trigger_type(),
            'trigger_setting': script_list[key].get_trigger_settings()
        }
        list_all.append(list_all_info)

    return flask.jsonify({'all': list_all, 'return': True})


@app.route('/script/<script_name>/run', methods=['GET'])
@crossdomain(origin='*')
def script_run(script_name):
    """
    DONE
    Adds script to the scriptList and creates an object
    """
    #TODO return text and valid from Script
    output = script_list[script_name].run()
    return_val = output[0]

    return flask.jsonify({'output': output[1], 'return': return_val})


@app.route('/script/<script_name>/add', methods=['GET'])
@crossdomain(origin='*')
def script_add(script_name):
    #TODO: REMOVE
    """
    NOT NEEDED
    Adds script to the scriptList and creates an object
    """

    if script_name in script_list:
        output = "Script has already been added"
        return_val = False
    else:
        script_list[script_name] = script.Script(script_name)
        output = "Script has been added"
        return_val = True

    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/script/<script_name>/enable', methods=['GET'])
@crossdomain(origin='*')
def script_enable(script_name):
    """
    DONE
    Enables script if configured
    """
    #TODO return text and valid from Script
    output = script_list[script_name].set_enabled()
    return_val = True

    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/script/<script_name>/disable', methods=['GET'])
@crossdomain(origin='*')
def script_disable(script_name):
    """
    DONE
    Disables script
    """
    #TODO return text and valid from Script
    output = script_list[script_name].set_disabled()
    return_val = True

    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/script/<script_name>/setting/<string:setting>/<int:value>', methods=['GET'])
@crossdomain(origin='*')
def script_set_trigger(script_name, setting, value):
    """
    DONE
    Set script trigger settings
    """
    #TODO return text and valid from Script
    output = script_list[script_name].set_trigger_setting(setting, value)
    return_val = True

    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/script/<script_name>/output/hist/<string:amount>', methods=['GET'])
@app.route('/script/<script_name>/output/hist/<string:amount>/<int:limit>', methods=['GET'])
@crossdomain(origin='*')
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
        log_.warning("func: getOutput("+script_name+", "+amount+")\\n\\t"+output)

    return flask.jsonify({'output': output, 'return': return_val})


@app.route('/script/<script_name>/output/live', methods=['GET'])
@crossdomain(origin='*')
def get_output_live(script_name):
    """
    DONE
    Get the live output
    """
    output = script_list[script_name].get_output()
    return_val = True

    return flask.jsonify({'output': output, 'return': return_val})


def add_scripts():
    for each_file in os.listdir("./scripts/"):
        file_name = os.path.splitext(os.path.basename(each_file))
        if file_name[1] == ".py" \
                and each_file != "__init__.py" \
                and each_file != "example.py":
            script_name = file_name[0]
            script_list[script_name] = script.Script(script_name)

if __name__ == '__main__':
    #set up general log file
    log_ = log.Log('./_log.db')
    #set up script history log
    hist = history.History('./scripts/_history.db')
    #dict to store scripts data
    script_list = {}
    add_scripts()

    log_.info("Main script started")
    app.run(debug=True)