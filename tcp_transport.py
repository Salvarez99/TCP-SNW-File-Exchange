from io import BufferedReader
import socket
import os
import sys
import tcp_transport


class TCP_Transport:

    def __init__(self) -> None:
        self.socket = None
        # self.client_path = "/home1/s/s/sa851266/project01/client_files"
        # self.server_path = "/home1/s/s/sa851266/project01/server_files"
        # self.cache_path = "/home1/s/s/sa851266/project01/cache_files"

        # "C:\Users\xenep\OneDrive\Documents\UAlbany\Fall_2023\ICSI_416_Computer_Communication_Networks\Projects\Project 01\Source\cache_files"
        self.client_path = "C:\\Users\\xenep\\OneDrive\Documents\\UAlbany\\Fall_2023\\ICSI_416_Computer_Communication_Networks\\Projects\\Project 01\\Source\\client_files"
        self.server_path = "C:\\Users\\xenep\\OneDrive\Documents\\UAlbany\\Fall_2023\\ICSI_416_Computer_Communication_Networks\\Projects\\Project 01\\Source\\server_files"
        self.cache_path = "C:\\Users\\xenep\\OneDrive\Documents\\UAlbany\\Fall_2023\\ICSI_416_Computer_Communication_Networks\\Projects\\Project 01\\Source\\cache_files"
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

        # if dest_path is not None:
        self.receiveFile(dest_path, self.socket)
        # else:
            #Path doesnt exist
            # pass

        response = self.receiveString(self.socket)
        print(response)

        pass

    """
    Client attempts to put file onto server
    """
    def tcp_client_put(self, file_name : str):
        """
        send sender

        TODO: Expect that the file is only sent here and storage is handled on receiver side
        send filename 
        check if file exist
            send file
        if not 
            exit
        
        receive response
        """

        sender = "client"
        self.sendString(sender, self.socket)
        print(f"Sending sender: {sender}")
        self.sendString(file_name, self.socket)
        print(f"Sending file name: {file_name}")

        
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

        print("In tcp_server")
        
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
                    TODO: Expect that the file is only sent here and storage is handled on receiver side 
                    while 
                        send file
                    send response
            else:
                quit
            """

            sender = self.receiveString(client_socket)

            if sender == "client":
                print(f"Sender is {sender}")
                file_name = self.receiveString(client_socket)
                print(f"Incoming file: {file_name}")
                dest_path = self.createDestinationPath(file_name, "server")
                print(f"Destination Path: {dest_path}")
                self.receiveFile(dest_path, client_socket)
                self.sendString("File Uploaded Sucessfully", client_socket)
                pass
            elif sender == "cache":
                file_name = self.receiveString(client_socket)
                file_path = self.fileExistInDir(file_name, "server")

                if file_path is not None:
                    self.sendFile(file_path, client_socket)
                    self.sendString("File delivered from origin.", client_socket)
                    # pass
            else:
                sys.exit()


    def tcp_cache_get(self, passed_socket : socket = None)-> bool:
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
            client_socket, address = self.socket.accept()
            sender = self.receiveString(client_socket)
            file_name = self.receiveString(client_socket)

            file_path = self.fileExistInDir(file_name, "cache")

            if file_path is not None:
                self.sendFile(file_path, client_socket)
                self.sendString("File delivered from cache.", client_socket)
            else:
                if isinstance(passed_socket, socket.socket):

                    sender = "cache"
                    self.sendString(sender, passed_socket)
                    self.sendString(file_name, passed_socket)

                    dest_path = self.createDestinationPath(file_name, "cache")
                    self.receiveFile(dest_path, passed_socket)


                    response = self.receiveString(passed_socket)
                    file_path = self.fileExistInDir(file_name, "cache")


                    self.sendFile(file_path, client_socket)
                    self.sendString(response, client_socket)

    """Put a file into the server directly from client
    Param1: filename: name of file being sent
    Param2: path: the path where the file is located ("server" | "cache" | "client")
    """
    def put(self, fileName: str, location_of_File: str, destination: str):
        """
        1. Designate which path we should look in to find the file that is going to be sent
        2. Find the file from specified path
            2.1a if the file exist, create str that has path + filename
            2.1b if the file doesn't exist, exit
            2.2a if the path is the client, create str but add "" + filename
        3. Send the destination ("server" | "cache" | "client") 
        3. Send the filename
        4. Send the size of file
        5. Send file
        6. Receive Response
        """

        """
        Example Send:
            Destination Path length 
            Destination Path (Used to open a file in this location)
            FileName Length
            FileName
            File Size
            File
        """
        # checks to see if the file from given path exist
        # otherwise exit program
        file_path = self.fileExistInDir(fileName, location_of_File)
        file_name = os.path.basename(file_path)

        # send the length of the destination and destination
        destination_path = self.createDestinationPath(file_name, destination)
        destination_path_length = str(len(destination_path)).zfill(10)
        self.socket.send(destination_path_length.encode())
        self.socket.send(destination_path.encode())

        # Send the length of the file name and file name
        file_name_length = str(len(file_name)).zfill(10)
        self.socket.send(file_name_length.encode())
        self.socket.send(file_name.encode())

        # Send the length of the file size and file size
        file_size = os.path.getsize(file_path)
        file_size_length = str(len(str(file_size))).zfill(10)
        self.socket.send(file_size_length.encode())
        self.socket.send(str(file_size).encode())

        # Send file over socket
        with open(file_path, "rb") as file:
            data = file.read(1024)
            while data:
                self.socket.send(data)
                data = file.read(1024)

        """
        TODO: Receive msg back either saying
        File Uploaded Successfully
        or 
        File Upload Failed
        """

        response_length = int(self.socket.recv(10))
        response = self.socket.recv(response_length).decode()
        print(response)

        pass

    def get(self):
        """
        Example Incoming data:
            Destination Path length 
            Destination Path (Used to open a file in this location)
            FileName Length
            FileName
            File Size
            File
        """

        """
        1. Receive Destination Path Length
        2. Receive Destination Path
        3. Receive FileName Length
        4. Receive FileName
        5. Receive File Size
        6. Receive File
        7. Send Response 
        """

        while True: 

            client_socket, address = self.socket.accept()

            dest_path_length = int(client_socket.recv(10))
            dest_path = client_socket.recv(dest_path_length).decode()

            file_name_length = int(client_socket.recv(10))
            file_name = client_socket.recv(file_name_length).decode()

            file_size_length = int(client_socket.recv(10))
            file_size = int(client_socket.recv(file_size_length))

            received_data = 0

            with open(dest_path, "wb") as file:
                while received_data < file_size:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    received_data += len(data)

            response = "File Uploaded Successfully"
            response_length = str(len(response)).zfill(10)

            client_socket.send(response_length.encode())
            client_socket.send(response.encode())

        pass

    def fileExistInDir(self, filename: str, location: str) -> str:
        directory_path = ""

        print("In fileExistInDir")

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
        print(f"File path: {file_path}")

        ans = os.path.exists(file_path)
        print(f"Ans: {ans}")

        if ans:
        # if os.path.exists(file_path):
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
        print(f"Sending string length: {string_len}")
        send_to_socket.send(string_len.encode())
        #send string
        print(f"Sending string: {string}")
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
        print(f"Receiving string length: {string_len}")

        #ex. recv(11 bytes)
        string = recv_socket.recv(string_len).decode()
        print(f"Receiving string: {string}")

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
        print(f"Sending file size length: {file_size_length}")
        send_to_socket.send(str(file_size).encode())
        print(f"Sending file size : {file_size}")

        print("Sending file")
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
        print(f"Incoming file size length: {file_size_length}")
        file_size = int(recv_socket.recv(file_size_length))
        print(f"Incoming file size: {file_size}")


        received_data = 0
        print("Receiving file")
        with open(dest_path, "wb") as file:
            while received_data < file_size:
                data = recv_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                received_data += len(data)
            print("File Received")
        pass

