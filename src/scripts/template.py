
class Template:
    """
    This is the framework for each script
    """
    def __init__(self):
        #keeps track of the scripts output
        self._outputData = []
        self.trigger = 'call'
        #used to stop any loops you may have
        self._running = True

    def _output(self, data):
        print(data)
        self._outputData.append(data)

    def get_output(self):
        return self._outputData

    def stop(self):
        self._running = False



