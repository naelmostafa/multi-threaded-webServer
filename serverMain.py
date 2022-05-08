from Server import Server
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        server = Server().start()
    if len(sys.argv) == 2:
        server = Server(sys.argv[1]).start()

    if len(sys.argv) > 2:
        print("Usage: python serverMain.py [port]")
        sys.exit(1)
