import socket
from multiprocessing import cpu_count, Manager
from threading import Thread
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# Constants
buff_size = 1024
server_host = "127.0.0.1"
server_port = 8801
        
def clientRequestReceiver(client_socket, request_queue):
    while True:
        request_data = client_socket.recv(buff_size).decode()
        
        if request_data is None or request_data == "EXIT":
            print("Client disconnected")
            break
        print("Proxy received request from client: "+request_data)
        
        request_queue.put((request_data, client_socket))
        
    client_socket.close()

def mainProcessHandler(request_queue):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(("0.0.0.0", 8800))
    proxy_socket.listen(5)
    print("Started proxy server")
    
    with ThreadPoolExecutor(max_workers=5) as request_receiver_thread_pool:        
        while True:
            print("Waiting for client connection")
            client_socket, client_address = proxy_socket.accept()
            print("Accepted a client connection from " + client_address[0] + ":" + str(client_address[1]))
            request_receiver_thread_pool.submit(clientRequestReceiver, client_socket, request_queue)
            
def sendClientRequest(request_data, client_socket, remote_socket):
    remote_socket.send(request_data.encode())
        
    response_data = remote_socket.recv(buff_size).decode()
    print("Proxy received response from server: "+response_data)

    client_socket.send(response_data.encode())

def handleRequest(remote_socket, request_queue):
    print("Initilaized processor")

    while True:
        request_data, client_socket = request_queue.get()
        sendClientRequest(request_data, client_socket, remote_socket)
        
def startRequestHandlersProcessors(request_queue):
    proccesors_num = int(cpu_count() / 2)
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((server_host, server_port))
    
    with ProcessPoolExecutor(max_workers=proccesors_num) as processor_pool:         
        for i in range(proccesors_num - 1):
            processor_pool.submit(handleRequest, remote_socket, request_queue)
        
def startProxyServer():
    request_queue = Manager().Queue()
    start_processes = Thread(target=startRequestHandlersProcessors, args=(request_queue,))
    start_processes.start()
    mainProcessHandler(request_queue)  
    
if __name__ == '__main__':
    startProxyServer()
