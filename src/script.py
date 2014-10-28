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
        self._next_run = None
        self._enabled = False
        self._thread = None
        self._running = False
        self._start_time = None
        self.trigger_type = None
        #import class from correct module
        module = importlib.import_module('scripts.'+self._name)
        self._c = getattr(module, self._name.title())
        self._script = self._c()
        self._check_trigger()

    def _exec(self):
        while self._enabled:
            self._running = True
            self._last_run = self._get_timestamp()
            self._script = self._c()
            self._script.run()
            self._running = False
            self._hist.save(self._name, self.get_output_all())
            if self._script.trigger == 'interval':
                self._next_run = int(time.time()+self._trigger['interval'])
                time.sleep(self._trigger['interval'])
            else:
                break

    def _start_thread(self):
        self._thread = threading.Thread(target=self._exec)
        self._thread.start()

    def run(self):
        """
        Only run is the script is 'enabled' and the trigger is 'call'
        """
        if self.is_enabled():
            if self.trigger_type == 'call':
                self._start_thread()
                output = "Script is set to run"
                return_val = True
            else:
                output = "Script cannot be called"
                return_val = False
        else:
            output = "Script is not enabled"
            return_val = False

        return [output, return_val]

    def stop(self):
        """
        Stops the script running in its place
        """
        try:
            self._script.stop()
            return ["Script 'stop' command sent", True]
        except:
            return ["Script cannot be stopped", False]

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
        else:
            pass

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_next_run(self):
        output = self._next_run
        return_val = True
        if self._script.trigger == 'call':
            output = "Called scripts do not have a next run time"
            return_val = False
        elif not self._next_run:
            output = "Script has not run yet"
            return_val = False

        return [output, return_val]

    def set_trigger_setting(self, setting, value):
        """
        Set trigger settings value
        Settings cannot be changed when script is enabled
        """
        if self.is_enabled():
            return ["Cannot edit script with enabled, first disable and try again.", False]

        if setting not in self.get_trigger_settings():
            return ["Script does not have setting: "+setting, False]

        self._trigger[setting] = value
        return [setting+" set to "+str(value), True]

    def set_enabled(self):
        """
        Enable Script, and if interval then start
        """
        if self.is_enabled():
            return ["Script is already enabled", False]

        enable_script = True
        output = ""
        trigger_settings = self.get_trigger_settings()
        for key in trigger_settings:
            if not trigger_settings[key]:
                enable_script = False
                output += key+", "

        if not enable_script:
            output += "needs to be set"
            return [output, False]

        self._enabled = True
        self._uptime = self._get_timestamp()
        if self.trigger_type == 'interval':
            self._start_thread()

        self._start_time = datetime.datetime.now().replace(microsecond=0)
        return ["Script is enabled", True]

    def set_disabled(self):
        """
        Disable Script
        """
        if not self.is_enabled():
            return ["Script is already disabled", False]

        self._enabled = False
        self._start_time = None
        return ["Script is disabled", True]

    def get_trigger_settings(self):
        """
        Returns the dict of trigger settings
        """
        return self._trigger

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
        if self._start_time:
            return str(datetime.datetime.now().replace(microsecond=0) - self._start_time)
        else:
            return '0:00:00'

    def get_last_run(self):
        return self._hist.get_last_run(self._name)

    def get_output_all(self):
        """
        Returns the live output of the script running up to this point
        """
        return self._script.get_output()

    def get_output(self):
        """
        Returns the most recent output of the script
        """
        return [self._script.get_output(), True]