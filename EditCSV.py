import csv
with open('cemetery.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    with open('cemetery_edited.csv', 'w') as output:
        for row in csv_reader:
            output.write('\t'.join(row[1:]) + '\t' + row[0]+'\n')
    output.close()