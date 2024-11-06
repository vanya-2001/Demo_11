# Syntax Sugar (синтаксический сахар)
# списочные выражения (list comprehensions)
# [выражение for переменная in источник if условие]

ipaddress = '192.168.0.1'
greet = 'Hello World'
# s = ipaddress.split('.')
# a = map(int, s)
# print(s)
a = [int(i) for i in ipaddress.split('.') if int(i) > 0]
b = [i for i in range(2, 11, 2)]
c = [i for i in greet if i.isupper()]  # isupper()
d = [(pos, char) for pos, char in enumerate(greet)]
# for i in range(1, 11):
#     a.append(i)

print(d)
