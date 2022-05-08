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
      
