
class Example:

    def __init__(self):
        self._output = []
        self.trigger = 'call'

    def run(self):
        """
        Main function that is called
        """
        self.output.append("I ran!")
        return self.output

    def get_output(self):
        return self._output