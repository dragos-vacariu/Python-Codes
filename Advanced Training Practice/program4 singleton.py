#Creating the singleton decorator.
def singleton(A):
    object = A()
    def proxy():
        return object
    return proxy


@singleton #the singleton is defined above
class A: pass # Singleton a class that will only be instaciated once, all references will point to same object.

b = A()
a = A()
print(a is b)

