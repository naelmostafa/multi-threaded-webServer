import sys
from Client import Client

if __name__ == '__main__':
    if len(sys.argv) == 4:
        method = sys.argv[1]
        file_name = sys.argv[2]
        server = sys.argv[3]
        client = Client(server=server).start(method=method, file_name=file_name)

    elif len(sys.argv) == 5:
        method = sys.argv[1]
        file_name = sys.argv[2]
        server = sys.argv[3]
        port = sys.argv[4]
        client = Client(server=server, port=port).start(method=method, file_name=file_name)

    else:

        print("Usage: python clientMain.py <method> <file_name> <server> <port=80>")
