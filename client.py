import sys
from tcp_transport import *

args = sys.argv
opt = ""

# Should also  check if each argument is valid
# TODO: ask about localhost and what we should be checking for other than length
if len(args) > 6 or len(args) < 6:
    print("Invalid argument length, Exiting.")
    sys.exit()
elif args[-1] != "tcp" and args[-1] != "snw":
    print("Invalid Protocol, Exiting.")
    sys.exit()

for arg in args:
    print(f"{arg}", end=" ")
print()

tcp = TCP_Transport(args[1], int(args[2]), args[3], int(args[4]))

while (opt != "quit"):
    opt = input("Enter command: ")
    command = opt.split(" ")

    # Assuming 2nd arg is valid filename
    if len(command) == 2:
        match command[0]:
            case "put":
                print("Awaiting server response.")
                if args[-1] == "tcp":
                    # TODO: Get and print server response
                    file = open(command[1], "rb")
                    tcp.clientPutTCP(file)
                    print("tcp: put")
                else:
                    # TODO: Get and print server response
                    print("snw: put")
                pass
            case "get":
                if args[-1] == "tcp":
                    # TODO: Get and print server response
                    print("tcp: get")
                else:
                    # TODO: Get and print server response
                    print("snw: get")
                pass
            case _:
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

# TODO: close all opened connections? might not have to do if I use "with"
print("Exiting program!")
