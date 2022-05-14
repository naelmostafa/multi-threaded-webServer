import sys
from Client import Client

"usage python client_test <input-file>"

if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
    else:
        input_file = input('Enter file name: ')
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line != '':
                    line = line.split(' ')
                    print(line)
                    method = line[0]
                    file_name = line[1]
                    server = line[2]
                    port = 80
                    if len(line) == 4:
                        port = int(line[3])
                    client = Client(server=server, port=port).start(method=method, file_name=file_name)
    except Exception as e:
        print(e)
