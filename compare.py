# csv file comparer, taken from https://stackoverflow.com/a/38996374

with open('old.csv', 'r') as f1, open('output.csv', 'r') as f2:
    fileone = f1.readlines()
    filetwo = f2.readlines()

with open('differences.csv', 'w') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)