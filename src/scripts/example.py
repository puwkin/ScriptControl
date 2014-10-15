
class Example:
    """
    This is the default structure for each module
    """
    def __init__(self):
        self._output = []
        #trigger:
        #   call     - only runs when called via api
        #   interval - runs every x seconds
        self.trigger = 'call'

    def run(self):
        """
        Main function that is called
        """
        self._output.append("I ran!")
        return self._output

    def get_output(self):
        return self._output