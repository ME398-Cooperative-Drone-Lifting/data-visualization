import csv
file = open('test.csv')
type(file)
csvreader = csv.reader(file)
header = []
header = next(csvreader)
header
rows = []
for row in csvreader:
    rows.append(row)
file.close()

print(rows)