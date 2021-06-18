import csv

with open('file.csv', mode='w') as f:
    fieldnames = ['emp_name', 'dept', 'birth_month']
    writer = csv.writer(f, delimiter=',', quotechar='"', fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)

    writer.writeheader()
    writer.writerows([['John Smith', 'Accounting', 'November'], ['Erica Meyers', 'IT', 'March']])

# import pandas
# open("data.csv", mode="w")
# df = pandas.read_csv('data.csv',
#             index_col='Employee',
#             parse_dates=['Hired'],
#             header=0,
#             names=['Employee', 'Hired', 'Salary', 'Sick Days'])
# df.to_csv('hrdata_modified.csv')