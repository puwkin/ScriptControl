import time


class Loop:

    def __init__(self):
        self._output = []
        self.trigger = 'call'
        self._running = True

    def run(self):
        for i in range(0, 10):
            if not self._running: break #break out of loop if called to do so
            print(i)
            self._output.append("Val: "+str(i))
            time.sleep(1)
        self._output.append("Done")
        return self._output

    def stop(self):
        self._running = False

    def get_output(self):
        return self._output
