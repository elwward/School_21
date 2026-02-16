import sys

def extractor(arg):
    with open(arg, 'r', encoding='utf-8') as f:
        line=f.read()

    new_line=''
    mail = ''
    index=0
    while index < len(line):
        s=line[index]
        if s=='.':
            new_line += line[:index].capitalize()+'\t'
            mail += line[:index+1]
            line=line[index+1:]

            index = 0
        elif s=='@':
            new_line+=line[:index].capitalize()+'\t'
            mail += line[:index] + "@corp.com\n"
            new_line += mail
            line = line[index+10:]
            mail = ''

            index = 0
        else: index+=1

    with open('employees.tsv', 'w', encoding='utf-8') as f:
        f.write(new_line)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments")

    extractor(sys.argv[1])