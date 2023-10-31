import sys
import socket
from tcp_transport import *

# TODO: Ask what about sys.argv we need to check
if len(sys.argv) > 3 or len(sys.argv) < 3:
    print("Invalid argument length, Exiting.")
    sys.exit()
elif sys.argv[-1] != "tcp" and sys.argv[-1] != "snw":
    print("Invalid Protocol, Exiting.")
    sys.exit()

for arg in sys.argv:
    print(f"{arg}", end=" ")
print()

#
# TODO: Can be UAlbany VM?
# HOST = "icsi416-fa23.its.albany.edu"
HOST = "localhost"
PORT = int(sys.argv[1])
serverTCP = TCP_Transport()
match sys.argv[len(sys.argv) - 1]:
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
