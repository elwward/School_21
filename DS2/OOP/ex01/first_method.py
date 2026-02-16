class Research():
    def file_reader(self):
        with open('../ex00/data.csv', 'r') as f:
            return f.read()

if __name__ == '__main__':
    #researcher=Research()
    #print(researcher.file_reader())
    try:
        researcher=Research().file_reader()
        print(researcher)
    except Exception as error:
        print(error)
