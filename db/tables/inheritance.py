#!/media/jll/Occam/dev/sandbox/bikedb/.venv/bin/python3

class Test(): 
    def __init__(self):
        self.one = 1
        self.two = 2
        self.three = 3
        self.l = [self.one, self.two, self.three]
        self.d = {'test': self.l}
        self.test = "this is a random variable."


class Sub(Test):
    def __init__(self):
        super().__init__()
        self.s = str(self.d)
        self.set_test()
        self.print_value()
    
    test = 'nope'

    def set_test(self):
        test = self.test
    
    def print_value(self): 
        print(self.s)
        print(test)