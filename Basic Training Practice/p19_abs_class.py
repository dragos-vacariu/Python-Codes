from abc import abstractmethod, ABC  # importing this to be able to create abstact methods

class PUNCT(ABC): #PUNCT will be abstract
    #constructor
    def __init__(self):
        self.x=0 #non-static field
        self.y=0 #non-static field

    @abstractmethod #this will make the following method abstract
    def abstract_method(self):
        pass