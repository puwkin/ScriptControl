import importlib
import threading
import time
import datetime
import history


class Script:
    """
    Handles all the data for the script
    """
    def __init__(self, script_name):
        self._hist = history.History('./scripts/_history.db')
        self._name = script_name
        self._trigger = {}
        self._enabled = False
        self._thread = None
        self._running = False
        self._uptime = 0
        self.trigger_type = None
        #import class from correct module
        module = importlib.import_module('scripts.'+self._name)
        c = getattr(module, self._name.title())
        self._script = c()
        self._check_trigger()

    def _exec(self):
        while self._enabled:
            self._hist.save(self._name, "Running")
            self._running = True
            self._script.run()
            self._running = False
            if self._script.trigger == 'interval':
                time.sleep(self._trigger['interval'])
            else:
                break

    def run(self):
        """
        Only run is the script is 'enabled' and the trigger is 'call'
        """
        if self.is_enabled():
            if self.trigger_type == 'call':
                self._thread = threading.Thread(target=self._exec)
                self._thread.start()
                output = "Script is set to run"
                return_val = True
            else:
                output = "Script cannot be called"
                return_val = False
        else:
            output = "Script is not enabled"
            return_val = False

        return [output, return_val]

    def _check_trigger(self):
        """
        Get the type of trigger the script responds to
        Types:
            call - only runs when called in the api
            interval - triggered at an interval
        """
        self.trigger_type = self._script.trigger
        if self.trigger_type == "interval":
            self._trigger['interval'] = None
            self._trigger['rand'] = 4
        else:
            pass

    def _set_uptime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_trigger_setting(self, setting, value):
        """
        Set trigger settings value
        Settings cannot be changed when script is enabled
        """
        if self.is_enabled():
            return "Cannot edit script with enabled, first disable and try again."

        if setting not in self.get_trigger_settings():
            return "Script does not have setting: "+setting

        self._trigger[setting] = value
        return setting+" set to "+str(value)

    def get_trigger_settings(self):
        """
        Returns the dict of trigger settings
        """
        return self._trigger

    def set_enabled(self):
        """
        Enable Script
        """
        if self.is_enabled():
            return "Script is already enabled"

        enable_script = True
        output = ""
        trigger_settings = self.get_trigger_settings()
        for key in trigger_settings:
            if not trigger_settings[key]:
                enable_script = False
                output += key+", "

        if not enable_script:
            output += "needs to be set"
            return output

        self._enabled = True
        self._uptime = self._set_uptime()
        return "script is enabled"

    def set_disabled(self):
        """
        Disable Script
        """
        if not self.is_enabled():
            return "Script is already disabled"

        self._enabled = False
        self._uptime = 0
        return "Script is disabled"

    def is_enabled(self):
        """
        Return enabled status
        """
        return self._enabled

    def is_running(self):
        return self._running

    def get_trigger_type(self):
        return self.trigger_type

    def get_uptime(self):
        return self._uptime

    def get_output_all(self):
        """
        Returns the live output of the script running up to this point
        """
        return self._script.get_output()

    def get_output(self):
        """
        Returns the most recent output of the script
        """
        return self._script.get_output()[-1]