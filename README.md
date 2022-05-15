# Multi-threaded web server

## Project structure
- Client
  - Client.py
    - Contains the main application to communicate with the server
  - Request.py
    - Contains the request class to build the request
  - ResponseParser.py
    - Extracts response headers and body
---
- Server
  - Server.py
    - Contains the main application to communicate with the client
  - Response.py
    - Contains the response class to build the response
    - RequestParser.py
      - Extracts request method, headers and body
---

## Server
- It is a standalone multi-threaded web server.
- It is capable of handling multiple clients simultaneously.
- It is capable of handling multiple requests simultaneously.
- Store POST request data in `storage-server` directory.
  - Create `storage-server` directory to use storage functionality.

## Client
- Standalone simple client that can be used to send requests to the server.
- Supports GET, POST methods.
- Supports caching using shelve which is persistence dictionary. 
  - Create `cache-client` directory to use caching functionality.
- Store response data in `storage-client` directory.
  - Create `storage` directory to use storage functionality.

## How to run the project
- Run the server:
  - python serverMain.py <port>
    - port: the port to run the server on (default: 80)
    - server IP: is set to localhost `socket.gethostbyname(socket.gethostname())`

- Run the client:
  - python clientMain.py <path> <port>
    - path: the path to the file to send to the server or receive from the server
    - port: the port to connect to the server on (default: 80)

## Disclaimer ⚠️
- This project is not meant to be a complete web server.
- Its purpose is to demonstrate the use of threads and sockets.
- Still under development and testing 🚧.
- Use at your own risk.

