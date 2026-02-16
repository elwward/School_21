import sys

class Research():
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise ValueError("File is empty")

        if len(lines) == 1:
            raise ValueError("File does not contain enough lines")

        header = lines[0]
        if header == "":
            raise ValueError("Header is empty.")
        head_and_tail = header.split(',')
        if len(head_and_tail) != 2 or head_and_tail[0].strip() == "" or head_and_tail[1].strip() == "":
            raise ValueError("Header doesn't contain two columns")

        for line in lines[1:]:
            if not line:
                raise ValueError("Empty line")
            parts = line.split(',')
            if len(parts) != 2:
                raise ValueError(f"Doesn't contain 2 columns")
            a, b = parts[0].strip(), parts[1].strip()
            if (a, b) != ('0', '1') or (a, b) != ('1', '0'):
                raise ValueError(f"Data is incorrect. Not 1,0 or 0,1")

        return ''.join(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    try:
        researcher=Research(sys.argv[1])
        print(researcher.file_reader())
    except Exception as error:
        print(error)
