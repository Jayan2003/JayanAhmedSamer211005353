import socket

def send_single_request(message):
    # Create and connect socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))


    client_socket.send(message.encode())

    
    response = client_socket.recv(1024).decode()
    print('Server replied:', response)

    
    client_socket.close()


send_single_request("status")

