from random import randint
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
        def __init__(self,data):
            self.data=data
        def counts(self):
            return [sum([i[0] for i in self.data]), sum([i[1] for i in self.data])]
        def fractions(self, count):
            return [count[0]*100/(count[0]+count[1]), count[1]*100/(count[1]+count[0])]

class Analytics(Research.Calculations):
    def predict_random(self, number):
        result=[]
        for _ in range(number):
            first=randint(0,1)
            if first == 0:
                second=1
            else:
                second=0
            result.append([first, second])
        return result

    def predict_last(self):
        return self.data[-1]



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    try:
        researcher=Research(sys.argv[1])
        data=researcher.file_reader()
        print(data)

        calculator = Research.Calculations(data)
        count=calculator.counts()
        print(f'{count[0]} {count[1]}')
        print(f'{calculator.fractions(count)[0]:.4f} {calculator.fractions(count)[1]:.4f}')

        analytics = Analytics(data)
        print(analytics.predict_random(3))
        print(analytics.predict_last())
    except Exception as error:
        print(error)
