import sys
from tcp_transport import *

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

serverTCP = TCP_Transport()
cacheTCP = TCP_Transport()

while (opt != "quit"):

    opt = input("Enter command: ")
    command = opt.split(" ")

    # Assuming 2nd arg is valid filename
    if len(command) == 2:
        if command[0] == "put":
            print("Awaiting server response.")
            if args[-1] == "tcp":
                file_name = command[1]
                serverTCP.connect(args[1], int(args[2]))
                serverTCP.tcp_client_put(file_name)
                serverTCP.close()

            else:
                print("snw: put")
                # call method to interact with server : tcp_server()
                    # perform interaction
                    # close socket (client)
            pass
        elif command[0] == "get":
            if args[len(args) - 1] == "tcp":
                file_name = command[1]
                cacheTCP.connect(args[3], int(args[4]))
                cacheTCP.tcp_client_get(file_name)
                cacheTCP.close()
            else:
                # TODO: Get and print server response
                print("snw: get")
                # call method to interact with cache : tcp_cache()
                    # perform interaction
                    # close socket (client)
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
