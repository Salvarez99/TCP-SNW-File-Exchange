import sys
import socket
from tcp_transport import *


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

HOST = "localhost"
# HOST = "169.226.22.10"
PORT = int(sys.argv[1])

# Create server socket and listen for connnections
serverTCP = TCP_Transport()

# Keep server active
while True:
    serverTCP.listen(HOST, PORT)
    serverTCP.tcp_server()
