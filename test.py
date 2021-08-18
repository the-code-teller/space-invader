class A:
    def __init__(self):
        self.a = 10
    
a = A()
print(a.a)
del a
print(a.a)
