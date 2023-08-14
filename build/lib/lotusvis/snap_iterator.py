


class Fn:

    """Iterator that gets the next timestep and returns a snap."""

    def __init__(self, fns: list, start=0):
        self.num = start
        self.fns = fns
    
    def __iter__(self):
        return self

    def __next__(self):
        id = self.num
        if id<len(self.fns):
            fn = self.fns[id]
            self.num+=1
            return fn
        else:
            raise StopIteration
            
