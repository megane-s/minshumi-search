from itertools import tee


def my_iter():
    print("before 1")
    yield 1
    print("before 2")
    yield 2
    print("before 3")
    yield 3


a, b, c, d = tee(my_iter(), 4)

print("for")
for i in a:
    print(i)
