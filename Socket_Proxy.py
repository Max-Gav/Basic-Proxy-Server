import socket
import threading
buff_size = 1024
server_host = "127.0.0.1"
server_port = 8801

def handleClientRequest(client_socket):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((server_host, server_port))
    print("Proxy connecting to the server")
    
    while True:
        print("Waiting for the client to send a request")
        request_data = client_socket.recv(buff_size).decode()
        if request_data is None:
            break
        print("Proxy received from client: "+request_data)
        
        remote_socket.send(request_data.encode())
        response_data = remote_socket.recv(buff_size).decode()

        if response_data is None:
            break
        print("Proxy received from server: "+response_data)
        
        client_socket.send(response_data.encode())
    
    client_socket.close()
    remote_socket.close()
    

def startProxyServer():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(("0.0.0.0", 8800))
    proxy_socket.listen(5)
    print("Starting a proxy server")
    
    while True:
        client_socket, client_address = proxy_socket.accept()
        print("Accepted a client connection from " + client_address[0] + ":" + str(client_address[1]))
        client_request_thread = threading.Thread(target=handleClientRequest, args=(client_socket))
        client_request_thread.start()
        
        

if __name__ == '__main__':
    startProxyServer()