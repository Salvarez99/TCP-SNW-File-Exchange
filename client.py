import sys
from tcp_transport import *
from snw_transport import *

args = sys.argv
opt = ""

if len(args) > 6 or len(args) < 6:
    print("Invalid argument length, Exiting.")
    sys.exit()
elif args[len(args) - 1] != "tcp" and args[len(args) - 1] != "snw":
    print("Invalid Protocol, Exiting.")
    sys.exit()

for arg in args:
    print(f"{arg}", end=" ")
print()

server_address = args[1]
server_port = int(args[2])
cache_address = args[3]
cache_port = int(args[4])

serverTCP = TCP_Transport()
cacheTCP = TCP_Transport()
clientUDP = UDP_Transport()

#_______
#Create a UDP socket
clientUDP.createSocket()

#_______

while (opt != "quit"):

    opt = input("Enter command: ")
    command = opt.split(" ")

    # Assuming 2nd arg is valid filename
    if len(command) == 2:
        if command[0] == "put":
            print("Awaiting server response.")
            if args[-1] == "tcp":
                file_name = command[1]
                serverTCP.connect(server_address, server_port)
                serverTCP.tcp_client_put(file_name)
                serverTCP.close()

            else:
                print("snw: put")
                """
                TCP connect to server
                TCP Send sender
                TCP Send filename 
                Client UDP.put(file path, server address)
                TCP Receive server response  
                Print server response
                Close UDP and TCP
                """
                file_name = command[1]
                serverTCP.connect(server_address, server_port)
                serverTCP.sendString("client", serverTCP.socket)
                serverTCP.sendString(file_name, serverTCP.socket)

                file_path = serverTCP.fileExistInDir(file_name, "client")

                if file_path is not None:
                    clientUDP.put(file_path, server_address)
                    response = serverTCP.receiveString(serverTCP.socket)
                    print(response)
                    clientUDP.close()
                    serverTCP.close()
                    pass
                else:
                    sys.exit()
            pass
        elif command[0] == "get":
            if args[len(args) - 1] == "tcp":
                file_name = command[1]
                cacheTCP.connect(cache_address, cache_port)
                cacheTCP.tcp_client_get(file_name)
                cacheTCP.close()
            else:
                print("snw: get")
                """
                TCP connect to cache
                TCP send sender to cache
                TCP send filename
                Client UDP.get(destination path, cache address)
                TCP receive cache response
                Close UDP and TCP
                """

                file_name = command[1]
                cacheTCP.connect(cache_address, cache_port)
                cacheTCP.sendString("client", cacheTCP.socket)
                cacheTCP.sendString(file_name, cacheTCP.socket)

                dest_path = cacheTCP.createDestinationPath(file_name, "client")
                clientUDP.get(dest_path, cache_address)
                response = cacheTCP.receiveString(cacheTCP.socket)
                print(response)
                clientUDP.close()
                cacheTCP.close()
                pass
            pass
        elif command[0] == "quit":
            print("Invalid Command, Exiting.")
            sys.exit()

    elif len(command) == 1 and command[0] == "quit":
        print("", end="")

    elif command[0] == "put" or command[0] == "get":
        print("Incorrect command syntax, Exiting")
        sys.exit()
    else:
        print("Invalid command, Exiting.")
        sys.exit()

print("Exiting program!")
