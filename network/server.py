import socket

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to localhost on port 9999
server_socket.bind(('127.0.0.1', 9999))
server_socket.listen(1)

print("TCP Server is running and waiting for a connection...")

# Accept a connection
conn, addr = server_socket.accept()
print(f"Connected by client IP: {addr[0]}, Port: {addr[1]}")

# Receive and parse HTTP request
data = conn.recv(1024).decode()
if not data:
    print(f"Connection closed by client {addr[0]}")
    conn.close()
    exit()

# Split request into lines
lines = data.split('\r\n')

request_line = lines[0]
print(f"Request Line: {request_line}")

print("HTTP Headers:")
for header_line in lines[1:]:
    if header_line == '':
        break
    print(header_line)

# send HTTP response with proper headers
response_body = "<h1>Hello from server!</h1>"
response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    f"Content-Length: {len(response_body)}\r\n"
    "\r\n"
    f"{response_body}"
)

conn.send(response.encode())

# Close connection
conn.close()
print("Server connection closed.")
