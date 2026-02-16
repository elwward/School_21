import sys

def for_letter(arg):
    with open('employees.tsv', 'r', encoding='utf-8') as f:
        name=True
        for line in f:
            mas = line.split()
            if mas[2]==arg:
                name=False
                print(f"Dear {mas[0]}, welcome to our team! "
                    "We are sure that it will be a pleasure to work with you. "
                    "That’s a precondition for the professionals that our company hires.")
        if name:
            raise ValueError("This mail adress doesn't exist.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments")

    for_letter(sys.argv[1])