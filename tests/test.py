class Test:

    def __call__(self, key):
        return key
p=Test()
print(p("foo"))
