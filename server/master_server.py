class A:
    
    def __init__(self, field1, b):
        self.field1 = field1
        self.b = b

class B:

    def __init__(self, field1):
        self.field1 = field1

b = B(1)
a = A(2, b)

print(a.__dict__)
print(b.__dict__)
