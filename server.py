import sys
import socket

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
HOST = "localhost"
PORT = args[1]

match args[-1]:
    case "tcp":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen()
            client, addr = sock.accept()
            # TODO: Send back appropriate message

        with client:

            newFile = open("receivedFile.txt", "wb")

            # receiving expected file length
            fileLength = client.recv(1024)
            print(f"Length of expected file: {fileLength.decode()}\n")

            # receiving expected file length
            fl = (int)(fileLength.decode())  # expected file size
            print("file-length:", fl)

            receivedDataSize = 0
            data = client.recv(1024)

            while data:

                # If no more data in socket, break
                if not data:
                    break

                else:
                    # print("data: ", data.decode())
                    receivedDataSize += len(data)

                    print(f"Data Received: {receivedDataSize}")
                    newFile.write(data)

                    """ We stop receving once we get the required bytes. 
                            Or else it will keep waiting for the data from the client"""
                    if (receivedDataSize < fl):
                        data = client.recv(1024)
                    else:
                        break

            newFile.close()
            print("File Closing")

            msg = "File Uploaded Successfully"
            client.send(msg.encode())

        pass
    case "snw":
        pass
    case _:
        sys.exit()
        pass
