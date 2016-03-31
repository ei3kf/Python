#!/usr/bin/python

def foobar(n):
    if n % 3 == 0:
        return "Foo"
    elif n % 5 == 0:
        return "Bar"


for n in range(1,16):
    print("N = {} FooBar = {}").format(n, foobar(n)) 
