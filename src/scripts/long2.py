import time


class Long2:

    def __init__(self):
        self._output = []
        self._count = 0
        self.trigger = 'interval'

    def run(self):
        for i in range(0, 10):
            self._count = i
            print i
            self._output.append("Val2: "+str(i))
            time.sleep(.5)
        self._output.append("Done")
        return self._output

    def get_output(self):
        return self._output
