from tcp_transport import *
from snw_transport import *


# Example cmd: ./cache.py 20000 localhost 10000 tcp
#                   0        1       2       3
# Command line error checking
if len(sys.argv) > 5 or len(sys.argv) < 5:
    print("Invalid argument length, Exiting.")
    sys.exit()
elif sys.argv[len(sys.argv) - 1] != "tcp" and sys.argv[len(sys.argv) - 1] != "snw":
    print("Invalid Protocol, Exiting.")
    sys.exit()

#Socket that connects to server
serverTCP = TCP_Transport()

#socket that listens for client connection
clientTCP = TCP_Transport()
HOST = "localhost"
PORT = int(sys.argv[1])

server_address = sys.argv[2]
server_port = int(sys.argv[3])

cacheUDP = UDP_Transport()
cacheUDP.createSocket()
cacheUDP.bind(HOST, PORT)

"""
while True: 
    if("SNW"):
        TCP Socket
        TCP Bind
        TCP Listen

        TCP Accept client connection

        TCP client socket recv sender
        TCP client socket recv filename

        If(cache has file):
            UDP.put(file path, client address)
            TCP send response to client
            Close UDP

        Else:
            TCP connect to server
            TCP send sender to server
            TCP send filename to server
            UDP.get(destination path)
            TCP get response from server
            TCP send response to client
            
            TCP close server socket

    elif("TCP"):
        TCP listen for client
        TCP cache_get()
"""

while True:
    if sys.argv[len(sys.argv - 1)] == "snw":
        clientTCP.listen(HOST, PORT)
        client_socket, address = clientTCP.socket.accept()

        sender = clientTCP.receiveString(client_socket)
        file_name =  clientTCP.receiveString(client_socket)

        file_path = clientTCP.fileExistInDir(file_name, clientTCP.cache_path)

        if file_path is not None:
            cacheUDP.put(file_path, address)
            clientTCP.sendString("File delivered from cache.", client_socket)
            cacheUDP.close()
            pass

        else:
            serverTCP.connect(server_address, server_port)
            serverTCP.sendString("cache", serverTCP.socket)
            serverTCP.sendString(file_name, serverTCP.socket)
            dest_path = serverTCP.createDestinationPath(file_name, "cache")

            cacheUDP.get(dest_path, server_address)
            response = serverTCP.receiveString(serverTCP.socket)
            clientTCP.sendString(response, client_socket)
            serverTCP.close()
            pass
        pass
    elif sys.argv[len(sys.argv - 1)] == "tcp":

    # while True:
        # print(f"Establishing Cache Server on \nHOST: {HOST}\nPORT: {PORT}")
        clientTCP.listen(HOST, PORT)
        clientTCP.tcp_cache_get(serverTCP, server_address, server_port)
        pass