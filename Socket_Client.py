import socket
buff_size = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8800))
print("Connecting to the proxy")

while True:
    print("Enter your name: ")
    user_name = input()
    
    client_socket.send(user_name.encode())
    
    response_data = client_socket.recv(buff_size).decode()
    print(response_data)