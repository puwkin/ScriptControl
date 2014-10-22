

class Test:

    def __init__(self):
        self._outputData = []
        self.trigger = 'interval'

    def get_output(self):
        return self._outputData

    def _output(self, data):
        self._outputData.append(data)

    def run(self):
        """
        Main function that is called
        """
        self._output("I ran!")


