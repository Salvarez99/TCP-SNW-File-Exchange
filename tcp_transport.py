from io import BufferedReader
import socket
import os
import sys


class TCP_Transport:

    def __init__(self) -> None:
        self.socket = None
        self.HEADERSIZE = 20
        pass

        """Connect to a Host
        """

    def connect(self, serverIP: str, ServerPort: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((serverIP, ServerPort))
        pass

        """Listening for connections
        """

    def listen(self, serverIP: str, serverPort: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((serverIP, serverPort))
        self.socket.listen()
        print("Listening...")
        pass

        """Put a file into the server directly from client
        """

    def put(self, filename: str, pathChoice: str):

        # client puts files into server_files
        # cache puts files into client_files
        # server puts files into client_files

        if pathChoice == "server":
            path = "/home1/s/s/sa851266/project01/server_files/"
        elif pathChoice == "cache":
            path = "/home1/s/s/sa851266/project01/cache_files/"
        else:
            path = "/home1/s/s/sa851266/project01/client_files/"
        # TODO: add functionality for server path
        # if serverpath place file in server files folder

        # dirlist = os.listdir(path)
        # if (filename in dirlist):

            # send file path
            sendPath = f"{len(filename):<{self.HEADERSIZE}}" + filename
            self.socket.send(sendPath.encode())

            # send filename
            sendfilename = f"{len(filename):<{self.HEADERSIZE}}" + filename
            self.socket.send(sendfilename.encode())

            # send file size
            file = open(filename, "rb")
            # get file size as string
            sizeOfFile = str(os.path.getsize(filename))
            print(f"Size of file: {sizeOfFile}")
            # add header
            sizeOfFile = f"{len(sizeOfFile):< {self.HEADERSIZE}}" + sizeOfFile
            self.socket.send(sizeOfFile.encode())

            # Sending file over socket
            data = file.read(1024)

            while data:
                if not data:
                    break
                self.socket.send(data)
                data = file.read(1024)

            message = self.socket.recv(1024)
            print(message.decode())
            # self.socket.close()
        # else:
            # sys.exit()
        pass

    def temp(self):
        while True:
            clientSocket, address = self.socket.accept()
            print("Connected to client")
            with clientSocket:

                full_msg = ""
                new_msg = True
                while True:

                    pathHeader = clientSocket.recv(1024)

                    if len(pathHeader) != 0:
                        print(pathHeader.decode())

                        if new_msg:
                            # print( f"File name header: {pathHeader[:self.HEADERSIZE].decode()}")
                            msg_len = int(pathHeader[:self.HEADERSIZE])
                            new_msg = False

                        full_msg += pathHeader.decode()

                        if len(full_msg) - self.HEADERSIZE == msg_len:
                            # print(
                            #     f"full msg received: {full_msg[self.HEADERSIZE:]}")
                            fileName = full_msg[self.HEADERSIZE:]
                            print(f"File Name: {fileName}")

                            new_msg = True
                            full_msg = ""

                        # --------------------------------------------------------

                        fileNameHeader = clientSocket.recv(1024)

                        print(fileNameHeader.decode())

                        if new_msg:
                            # print( f"File name header: {fileNameHeader[:self.HEADERSIZE].decode()}")
                            msg_len = int(fileNameHeader[:self.HEADERSIZE])
                            new_msg = False

                        full_msg += fileNameHeader.decode()

                        if len(full_msg) - self.HEADERSIZE == msg_len:
                            # print(
                            #     f"full msg received: {full_msg[self.HEADERSIZE:]}")
                            fileName = full_msg[self.HEADERSIZE:]
                            print(f"File Name: {fileName}")

                            new_msg = True
                            full_msg = ""

                        # --------------------------------------------------------

                        sizeOfFile = clientSocket.recv(1024)
                        # print(sizeOfFile.decode())

                        if new_msg:
                            # print(f"new message length: {sizeOfFile[:self.HEADERSIZE].decode()}")
                            msg_len = int(sizeOfFile[:self.HEADERSIZE])
                            new_msg = False

                        full_msg += sizeOfFile.decode()

                        if len(full_msg) - self.HEADERSIZE == msg_len:
                            # print(
                            #     f"full msg received: {full_msg[self.HEADERSIZE:]}")
                            sizeOfFile = int(full_msg[self.HEADERSIZE:])
                            receivedDataSize = 0
                            print(
                                f"Incoming file size: {sizeOfFile}\n\n")

                            new_msg = True
                            full_msg = ""

                            # TODO: uncomment and change dir to put file in correct place
                            # newFile = open(fileName, "wb")
                            newFile = open("receivedFile.txt", "wb")

                            while True:
                                print(f"data received: {receivedDataSize}")
                                print(f"size of file: {sizeOfFile}")
                                data = clientSocket.recv(1024)
                                receivedDataSize += len(data)

                                newFile.write(data)
                                if receivedDataSize == sizeOfFile:
                                    receivedDataSize + 20
                                    break
                                if receivedDataSize > sizeOfFile:
                                    break

                            newFile.close()

                            reMessage = "File Successfully Uploaded"

                            clientSocket.send(reMessage.encode())
                            print("done")
                            # clientSocket.close()
                            # self.socket.close()

                        break
                # Cant break on line 145, will close the socket so client will not be able to connect again afterwards

        pass

        """Gets a file from either cache or server dependent on if cache has file or not
        """
    def get():
        pass

        """Get file from cache. If the file is on the cache send the file to the client.
        If the file is not on the cache, request the file from the server then send the file to the client
        """
    def getFromCache():
        pass

        """Get requested file from server and sends it to the cache
        """
    def getFromServer():
        pass
