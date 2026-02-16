import sys

def encode(argument,number,answer):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for i, letter in enumerate(argument):
        #letter.isascii() True, если символ входит в ASCII
        if letter.isalpha() and not ('a' <= letter <= 'z' or 'A' <= letter <= 'Z'):
            raise ValueError("The script does not support your language yet")

        try:
            a = alphabet.index(letter.lower())
        except ValueError:
            a = -1

        if letter.isupper() and a + number < len(alphabet):
            answer += alphabet[a + number].upper()
        elif letter.isupper() and a + number >= len(alphabet):
            answer += alphabet[a + number - len(alphabet)].upper()
        elif letter.islower() and a + number < len(alphabet):
            answer += alphabet[a + number]
        elif letter.islower() and a + number >= len(alphabet):
            answer += alphabet[a + number - len(alphabet)]
        else:
            answer += letter

    print(answer)

def decode(argument,number,answer):
    for i in argument:
        if i.isalpha() and not ('a' <= i <= 'z' or 'A' <= i <= 'Z'):
            raise ValueError("The script does not support your language yet")

        if i.islower():
            shifted = (ord(i) - ord('a') - number + 26) % 26
            answer += chr(ord('a') + shifted)
        elif i.isupper():
            shifted = (ord(i) - ord('A') - number + 26) % 26
            answer += chr(ord('A') + shifted)
        else:
            answer += i
    print(answer)

def caesar():
    if len(sys.argv) != 4:
        raise ValueError("You must enter three arguments")

    action = sys.argv[1]
    argument = sys.argv[2]
    number = int(sys.argv[3])

    answer=''

    if action == 'encode':
        encode(argument, number, answer)

    if action == 'decode':
        decode(argument, number, answer)

if __name__ == '__main__':
    caesar()