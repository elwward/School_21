import sys

class Research():
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header=True):
        with open(self.path, 'r') as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise ValueError("File is empty")

        if len(lines) == 1:
            raise ValueError("File does not contain enough lines")

        header = lines[0].strip().split(',')
        if len(header) != 2 or header != ['head', 'tail']:
            has_header = False

        if has_header:
            data=lines[1:]
        else:
            data=lines

        for line in data:
            if not line:
                raise ValueError("Empty line")
            parts = line.split(',')
            if len(parts) != 2:
                raise ValueError(f"Doesn't contain 2 columns")
            a, b = parts[0].strip(), parts[1].strip()
            if (a, b) != ('0', '1') and (a, b) != ('1', '0'):
                raise ValueError(f"Data is incorrect. Not 1,0 or 0,1")

        return [list(map(int, i.strip().split(","))) for i in data]

    class Calculations:
        def counts(self, data):
            return [sum([i[0] for i in data]), sum([i[1] for i in data])]
        def fractions(self, count):
            #count[0]+count[1]=len(lines)
            return [count[0]*100/(count[0]+count[1]), count[1]*100/(count[1]+count[0])]



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    try:
        researcher=Research(sys.argv[1])
        calculator=Research.Calculations()
        data=researcher.file_reader()
        print(data)
        count=calculator.counts(data)
        print(f'{count[0]} {count[1]}')
        print(f'{calculator.fractions(count)[0]:.4f} {calculator.fractions(count)[1]:.4f}')
    except Exception as error:
        print(error)
