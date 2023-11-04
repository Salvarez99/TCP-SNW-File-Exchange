import sys
from tcp_transport import *
from snw_transport import *



# Example cmd: ./server.py 20000 tcp
#                  0         1   2
# Command line error checking
if len(sys.argv) > 3 or len(sys.argv) < 3:
    print("Invalid argument length, Exiting.")
    sys.exit()
elif sys.argv[len(sys.argv) - 1] != "tcp" and sys.argv[len(sys.argv) - 1] != "snw":
    print("Invalid Protocol, Exiting.")
    sys.exit()

# Print out commands
for arg in sys.argv:
    print(f"{arg}", end=" ")
print()

# HOST = "localhost"
HOST = "169.226.22.10"
PORT = int(sys.argv[1])

# Create server socket and listen for connnections
serverTCP = TCP_Transport()
serverUDP = UDP_Transport()

serverUDP.createSocket()
serverUDP.bind(HOST, PORT)

"""
while True: 
    If ("TCP"):
        keep the same
    Elif ("UDP"):
            TCP listen
            TCP accept
    
            recv sender
            recv filename
    
            if(sender is client):
                UDP.get(destination path)
                TCP send response to client
                Close UDP
    
            elif(sender is cache):
                UDP.put(file path, address)
                TCP send response to cache
"""
while True: 
    if sys.argv[len(sys.argv - 1)] == "tcp":
        serverTCP.listen(HOST, PORT)
        serverTCP.tcp_server()
        pass
    elif sys.argv[len(sys.argv - 1)] == "snw":
        serverTCP.listen(HOST,PORT)
        incoming_socket, address = serverTCP.socket.accept()

        sender = serverTCP.receiveString(incoming_socket)
        file_name = serverTCP.receiveString(incoming_socket)

        if sender == "client":
            dest_path = serverTCP.createDestinationPath(file_name, "server")
            serverUDP.get(dest_path, address)
            serverTCP.sendString("File successfully uploaded.", incoming_socket)
            serverUDP.close()
            pass
        elif sender == "cache":
            file_path = serverTCP.fileExistInDir(file_name, "server")

            if file_path is not None:
                serverUDP.put(file_path, address)
                serverTCP.sendString("File delivered from origin.", incoming_socket)
                serverUDP.close()
                pass
            else:
                sys.exit()
            pass

        pass
