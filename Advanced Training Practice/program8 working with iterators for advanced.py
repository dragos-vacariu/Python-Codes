class Primes:
    def __init__(self, number):
        self.max = number
        self.current = 0

    def __iter__(self):
        self.current=0
        return self

    def __next__(self):
        if self.current-1 == self.max: raise StopIteration
        x = self.current
        self.current+=1
        return x


for prime in Primes(100):
    print(prime)

'''
Translation: 
it = iter(Prime(100)) #equivalent to it = Prime(100).__iter__()

while True:
    try:
        print(next(it))
    except StopIteration:
        break
'''


#print(len("string Value"))
'''Translated as print("string Value".__len__())'''