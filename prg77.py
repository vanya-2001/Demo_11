# csv - comma separated values
import csv

with open('personal.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';', quotechar='"')
    row = list(reader)
    for r in row:
        print(r['ПОЛ'])
