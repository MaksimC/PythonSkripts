def printhelloworld(string):
    print(string)


printhelloworld("Hello, World. This is my first python calculator.")

x = int(input("Input X: "))
y = int(input("Input Y: "))

action = int(input("Inout number of action that you want to do:\n"
                   "1. Sum\n"
                   "2. Minus\n"
                   "3. Multiply\n"
                   "4. Divide\n"))


def sumup(x, y):
    result = x + y
    print("result is: ", result)


def minus(x, y):
    result = x - y
    print("result is: ", result)


def multiply(x, y):
    result = x * y
    print("result is: ", result)


def divide(x, y):
    result = x / y
    print("result is: ", result)


if action == 1:
    sumup(x, y)
elif action == 2:
    minus(x, y)
elif action == 3:
    multiply(x, y)
elif action == 4:
    divide(x, y)
else:
    print("choose correct option")