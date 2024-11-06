# Декораторы
import time


def uppercase(func):
    def wrapper():  # обертка
        origin = func()
        modified = origin.upper()  # + ' декоратор'
        return modified

    return wrapper


def time_measure(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f'Затраченное время: {end - start}')

    return wrapper


@uppercase
def say_hello():
    return 'Hello'

@time_measure
def make_list():
    a = [i for i in range(5000000)]
    return a


# print(say_hello())
make_list()
