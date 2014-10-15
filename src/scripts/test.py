

class Test:

    def __init__(self):
        self.output = []
        self.trigger = 'call'

    def run(self):
        """
        Main function that is called
        """
        self.output.append("I ran!")
        return self.output

    def get_output(self):
        return self.output