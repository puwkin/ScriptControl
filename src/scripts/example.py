import time


class Example:
    """
    This is the default structure for each script
    """
    def __init__(self):
        #keeps track of the scripts output
        self._outputData = []
        #trigger:
        #   call     - only runs when called via api
        #   interval - runs every x seconds set by the api
        self.trigger = 'call'
        #used to stop any loops you may have
        self._running = True

    def _output(self, data):
        self._outputData.append(data)

    def get_output(self):
        return self._outputData

    def stop(self):
        self._running = False

    def run(self):
        """
        Main function that is called
        Your code here
        """
        self._output("I am running")
        for i in range(10):
            #use this if stmt where you want to exit your script if stopped is called
            if not self._running: break
            self._output("Val: "+str(i))
            time.sleep(1)

        self._output("I am done")


