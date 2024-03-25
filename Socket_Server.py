import socket
buff_size = 1024

def startBasicServer():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0",8801))
    server_socket.listen(15)
    print("Started basic server")

    while True:
        client_socket, client_address = server_socket.accept()
        print("Accepted a proxy connection from " + client_address[0] + ":" + str(client_address[1]))
        
        while True:
            request_data = client_socket.recv(1024).decode()
            if request_data is None:
                break
            
            response_data = "Hello " + request_data
            print("Returning to the proxy: "+response_data)
            client_socket.send(response_data.encode())
    
    
if __name__ == "__main__":
    startBasicServer()