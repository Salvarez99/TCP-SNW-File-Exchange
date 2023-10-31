import sys
import socket
from tcp_transport import *

args = sys.argv

# TODO: Ask what about args we need to check
if len(args) > 3 or len(args) < 3:
    print("Invalid argument length, Exiting.")
    sys.exit()
elif args[-1] != "tcp" and args[-1] != "snw":
    print("Invalid Protocol, Exiting.")
    sys.exit()

for arg in args:
    print(f"{arg}", end=" ")
print()

# TODO: Can be UAlbany VM?
# HOST = "icsi416-fa23.its.albany.edu"
HOST = "localhost"
PORT = int(args[1])
serverTCP = TCP_Transport()
match args[len(args) - 1]:
    case "tcp":
        serverTCP.listen(HOST,PORT)
        #Call method to send receive file
        serverTCP.temp()

        pass
    case "snw":
        pass
    case _:
        sys.exit()
        pass
