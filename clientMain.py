import Client
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 clientMain.py <server_ip> <server_port>")
        exit(1)
    else:
        server_ip = sys.argv[1]
        server_port = sys.argv[2]
        client = Client.Client(server_ip, server_port).start()
