def replace():
    #with open('ds.csv', 'r', encoding='utf-8') as f:
    #print(f.read())
    f = open('ds.csv', 'r', encoding='utf-8')
    line = f.read()
    f.close()

    k=0
    new_line=''
    for s in line:
        if s=='"' and k==0:
            k=1
        elif s=='"' and k==1:
            k=0

        if k==0 and s==',':
            new_line+='\t'
        else:
            new_line+=s

    f = open('ds.tsv', 'w', encoding='utf-8')
    f.write(new_line)
    f.close()

if __name__ == '__main__':
    replace()