from io import BufferedReader
import socket
import os
import sys


class TCP_Transport:

    def __init__(self) -> None:
        self.socket = None
        self.HEADERSIZE = 20
        self.client_path = "/home1/s/s/sa851266/project01/client_files"
        self.server_path = "/home1/s/s/sa851266/project01/server_files"
        self.cache_path = "/home1/s/s/sa851266/project01/cache_files"
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

        if location == "server":
            directory_path = self.server_path

        elif location == "cache":
            directory_path = self.cache_path

        elif location == "client":
            return filename

        else:
            sys.exit()

        absolute_dir_path = os.path.abspath(directory_path)
        file_path = os.path.join(absolute_dir_path, filename)

        if os.path.exists(file_path):
            return file_path

        return sys.exit()

    def createDestinationPath(self, filename: str, destination: str) -> str:
        directory_path = ""

        if destination == "server":
            directory_path = self.server_path

        elif destination == "cache":
            directory_path = self.cache_path

        elif destination == "client":
            # TODO: uncomment after testing  directory_path = self.client_path
            directory_path = ""

        else:
            sys.exit()

        absolute_dir_path = os.path.abspath(directory_path)
        destination_path = os.path.join(absolute_dir_path, filename)

        return destination_path
