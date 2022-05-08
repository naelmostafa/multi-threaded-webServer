import sys
from Client import Client

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python clientMain.py <server_ip> <server_port>")
        exit(1)
    else:
        try:
            server_ip = sys.argv[1]
            server_port = int(sys.argv[2])
        except ValueError:
            print("server_ip and server_port must be integers")
        else:
            client = Client(server_ip, server_port).start()
