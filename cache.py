from tcp_transport import *

"""
Error check commands

Create socket
Connect to server

Listen for connection

tcp_cache()


"""
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
serverTCP.connect(sys.argv[2], int(sys.argv[3]))

#socket that listens for client connection
clientTCP = TCP_Transport()
clientTCP.listen("localhost", int(sys.argv[1]))

while True:
    clientTCP.tcp_cache_get(serverTCP.socket)
