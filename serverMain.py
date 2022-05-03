import Server
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        server = Server.Server().start()
    if len(sys.argv) == 2:
        server = Server.Server(sys.argv[1]).start()

    if len(sys.argv) > 2:
        print("Too many arguments")
