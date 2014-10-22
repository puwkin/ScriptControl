import time


class Loop:

    def __init__(self):
        self._outputData = []
        self.trigger = 'call'
        self._running = True

    def stop(self):
        self._running = False

    def get_output(self):
        return self._outputData

    def _output(self, data):
        self._outputData.append(data)

    def run(self):
        for i in range(0, 10):
            if not self._running: break #break out of loop if called to do so
            print(i)
            self._output("Val: "+str(i))
            time.sleep(1)

        if not self._running:
            self._output("Stopped")
        else:
            self._output("Completed")



