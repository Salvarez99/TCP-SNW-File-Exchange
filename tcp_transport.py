import socket
import os
import sys


class TCP_Transport:

    def __init__(self) -> None:
        self.socket = None

        #VM paths
        self.server_path = "../server_files"
        # self.cache_path = "../cache_files"
        # self.client_path = "../client_files"

        #local paths
        # self.server_path = ".\\server_files"
        self.cache_path = ".\\cache_files"
        self.client_path = ".\\client_files"
        pass

    """Connect to a Host
    """
    def connect(self, serverIP: str, ServerPort: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((serverIP, ServerPort))
        pass

    """
    Listening for connections
    """
    def listen(self, serverIP: str, serverPort: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((serverIP, serverPort))
        self.socket.listen()
        print("Listening...")
        pass

    def close(self):
        self.socket.close()
        print("Connection closed")
        pass

    """
    Client attempts to get file from cache
    """
    def tcp_client_get(self, file_name : str):
        """
        send sender 
        send filename
        
        receive file 
        receive response
        
        """

        self.sendString("client", self.socket)
        self.sendString(file_name, self.socket)

        dest_path = self.createDestinationPath(file_name, "client")

        self.receiveFile(dest_path, self.socket)

        response = self.receiveString(self.socket)
        print(response)
        pass

    """
    Client attempts to put file onto server
    """
    def tcp_client_put(self, file_name : str):
        """
        send sender

        Expect that the file is only sent here and storage is handled on receiver side
        send filename 
        check if file exist
            send file
        if not 
            exit
        
        receive response
        """

        sender = "client"
        self.sendString(sender, self.socket)
        self.sendString(file_name, self.socket)

        
        file_path = self.fileExistInDir(file_name, sender)

        if file_path is not None:
            self.sendFile(file_path, self.socket)
        else:
            sys.exit()

        server_response = self.receiveString(self.socket)
        print(server_response)
        self.socket.close()

        pass

    def tcp_server(self):
        while True:
            print("Attempting to accept connections")
            client_socket, address = self.socket.accept()
            print("Connection established")

            """
            Receive sender

            if client:
                receive file name
                cerate destination path
                open new file in storage location
                while
                    receive file
                    write to opened file
                send response

            elif cache:
                receive filename
                if (file exist)/(look for file):
                    Expect that the file is only sent here and storage is handled on receiver side 
                    while 
                        send file
                    send response
            else:
                quit
            """

            sender = self.receiveString(client_socket)

            if sender == "client":
                file_name = self.receiveString(client_socket)
                dest_path = self.createDestinationPath(file_name, "server")
                self.receiveFile(dest_path, client_socket)
                self.sendString("File successfully uploaded.", client_socket)
                pass
            elif sender == "cache":
                file_name = self.receiveString(client_socket)
                file_path = self.fileExistInDir(file_name, "server")

                if file_path is not None:
                    self.sendFile(file_path, client_socket)
                    self.sendString("File delivered from origin.", client_socket)
            else:
                sys.exit()


    def tcp_cache_get(self, server_connection, serverIP : str, serverPort : int):
        """
        While true 
            accept connections 
            receive sender 
            receive filename
            
            if (file exist)
                send file to client
                send response to client
            else
                send sender to server 
                send filename to server

                open new file with filename in storage location
                while
                    receive file 
                    write to opened file
                receive response

                send file to client 
                send response to client
        """

        while True: 
            print("Attempting to accept connections")
            client_socket, address = self.socket.accept()
            print("Connection established")

            sender = self.receiveString(client_socket)
            file_name = self.receiveString(client_socket)

            file_path = self.fileExistInDir(file_name, "cache")

            if file_path is not None:
                self.sendFile(file_path, client_socket)
                self.sendString("File delivered from cache.", client_socket)
            else:
                if isinstance(server_connection, TCP_Transport):

                    server_connection.connect(serverIP, serverPort)

                    sender = "cache"
                    self.sendString(sender, server_connection.socket)
                    self.sendString(file_name, server_connection.socket)

                    dest_path = self.createDestinationPath(file_name, "cache")
                    self.receiveFile(dest_path, server_connection.socket)


                    response = self.receiveString(server_connection.socket)
                    file_path = self.fileExistInDir(file_name, "cache")


                    self.sendFile(file_path, client_socket)
                    self.sendString(response, client_socket)
                    server_connection.close()


    def fileExistInDir(self, filename: str, location: str) -> str:
        directory_path = ""

        if location == "server":
            directory_path = self.server_path

        elif location == "cache":
            directory_path = self.cache_path

        elif location == "client":
            directory_path = self.client_path
            # return filename
        else:
            sys.exit()

        absolute_dir_path = os.path.abspath(directory_path)
        # print(f"Abs Dir Path: {absolute_dir_path}")

        file_path = os.path.join(absolute_dir_path, filename)
        # print(f"File path: {file_path}")

        ans = os.path.exists(file_path)
        # print(f"Ans: {ans}")

        if ans:
            return file_path

        return None


    """
    Creates a destination path on where to store the file
    Ex. path/to/storage/filename.txt
    """
    def createDestinationPath(self, filename: str, destination: str) -> str:
        directory_path = ""

        if destination == "server":
            directory_path = self.server_path

        elif destination == "cache":
            directory_path = self.cache_path

        elif destination == "client":
            directory_path = self.client_path

        else:
            sys.exit()

        absolute_dir_path = os.path.abspath(directory_path)
        destination_path = os.path.join(absolute_dir_path, filename)

        # print(f"Destination Path: {destination_path}")

        return destination_path


    """
    Send a string over the socket to specified destination. String typically will be the sender, filename or response.
    Param1: String being sent
    Param2: Destination
    """
    def sendString(self, string : str, send_to_socket : socket):
        """
        1. Find size of string
        2. Send size of string
        3. Send string
        """

        #ex. 0000000011
        string_len = str(len(string)).zfill(10)
        #ex. send 0000000011
        # print(f"Sending string length: {string_len}")
        send_to_socket.send(string_len.encode())
        #send string
        # print(f"Sending string: {string}")
        send_to_socket.send(string.encode())

        pass

    """
    Receive a string from the socket. String typically will be the sender, filename or response.
    """
    def receiveString(self, recv_socket : socket) -> str:
        """
        1. Receive size of string
        2. Receive string
        3. Return string
        """
        #ex. 0000000011 -> 11
        string_len = int(recv_socket.recv(10).decode())
        # print(f"Receiving string length: {string_len}")

        #ex. recv(11 bytes)
        string = recv_socket.recv(string_len).decode()
        # print(f"Receiving string: {string}")

        return string

    """
    Send a file over the socket to specified destination.
    Param1: String being sent
    Param2: Destination
    """
    def sendFile(self, file_path : str, send_to_socket : socket):
        """
        1. Get file size
        2. Send file size
        3. Send file
        """

        file_size = os.path.getsize(file_path)
        file_size_length = str(len(str(file_size))).zfill(10)
        send_to_socket.send(file_size_length.encode())
        # print(f"Sending file size length: {file_size_length}")
        send_to_socket.send(str(file_size).encode())
        # print(f"Sending file size : {file_size}")

        # print("Sending file")
        with open(file_path, "rb") as file:
            data = file.read(1024)
            while data:
                send_to_socket.send(data)
                data = file.read(1024)
        pass

    """
    Receive a file from the socket.
    """
    def receiveFile(self, dest_path : str ,recv_socket : socket):
        """
        1. Receive file size
        2. Receive file 
        3. Store file
        """
        
        file_size_length = int(recv_socket.recv(10).decode())
        # print(f"Incoming file size length: {file_size_length}")
        file_size = int(recv_socket.recv(file_size_length))
        # print(f"Incoming file size: {file_size}")


        received_data = 0
        # print("Receiving file")
        with open(dest_path, "wb") as file:

            data_left = file_size
            # print(f"Total data to receive: {data_left}")

            while received_data < file_size:
                if data_left < 1024:
                    data = recv_socket.recv(data_left)
                    file.write(data)
                    received_data += data_left
                    # print(f"Received data: {received_data}")
                else:
                    data = recv_socket.recv(1024)
                    file.write(data)
                    received_data += len(data)
                    data_left -= len(data)
                    # print(f"Received data: {received_data}")
                    # print(f"Data left: {data_left}")

            # print("File Received")
        pass

