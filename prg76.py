# Умножение списка на число = повторяющийся значения в списке
# a = [0, 1] * 5
# a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# csv - comma separated values

with open('personal.csv', encoding='utf-8') as f:
    text = f.read()

table = [r.split(';') for r in text.split('\n')]
print(table[2][1])
