import sys
import socket
from tcp_transport import *

import sys

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python server.py <port> <connection_type>")
        sys.exit(1)

    # Parse command-line arguments
    PORT = int(sys.argv[1])
    connection_type = sys.argv[2]
    HOST = "169.226.22.10"


    # Validate connection type
    if connection_type not in ["tcp", "snw"]:
        print("Invalid connection type. Choose either 'tcp' or 'snw'.")
        sys.exit(1)

    # Your server logic goes here
    print(f"Server started on port {PORT} with connection type {connection_type}")
    serverTCP = TCP_Transport()



    #Only time I need to check connection type is when using put command
    if sys.argv[len(sys.argv) - 1] == "tcp":
        serverTCP.listen(HOST, PORT)
        # serverTCP.listen("localhost", PORT)
        serverTCP.get()

    elif sys.argv[len(sys.argv) - 1] == "snw":
        pass
    else:
        sys.exit()



if __name__ == "__main__":
    main()
