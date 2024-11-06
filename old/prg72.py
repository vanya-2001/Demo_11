# Syntax Sugar (синтаксический сахар)
# функции высшего порядка map и filter
users = [
    {'name': 'Igor', 'age': 25},
    {'name': 'Vova', 'age': 5},
    {'name': 'Matew', 'age': 16},
    {'name': 'Ivan', 'age': 11},
]

filtered_users = filter(lambda u: 6 < u['age'] < 16, users)
print(list(filtered_users))
#
# lambda a, b: a + b
#
# def ala_lambda(a, b):
#     return a + b

