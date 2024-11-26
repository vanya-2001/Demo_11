# r - строка (raw - "сырая")
import re  # regular expressions (поиск по образцу)

# pattern = r'\b\w{3}\b' # слова из 3 букв
# pattern = r'[0-5][0-9]'  # все цифры от 0 до 59
# ? аналог от 0 до 1
pattern = '<img[^>]+src="([^">]+)"'
test_string = 'Картинка <img src="bg.jpg"> в тексте</p>'
result = re.findall(pattern, test_string)

print(result)
