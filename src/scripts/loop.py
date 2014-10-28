import time
from .template import Template

class Loop(Template):

    def __init__(self):
        Template.__init__(self)

    def run(self):
        #Your code here...
        for i in range(0, 10):
            if not self._running: break #break out of loop if called to do so
            self._output("Val: "+str(i))
            time.sleep(1)

        if not self._running:
            self._output("Stopped")
        else:
            self._output("Completed")



