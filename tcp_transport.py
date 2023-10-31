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
    def put(self, fileName : str, path : str):

        """
        1. Designate which path we should look in to find the file that is going to be sent
        2. Find the file from specified path
            2.1a if the file exist, create str that has path + filename
            2.1b if the file doesn't exist, exit
            2.2a if the path is the client, create str but add "" + filename
        3. Send the filename
        4. Send the size of file
        5. Send file
        
        """
        #checks to see if the file from given path exist
        #otherwise exit program
        file_path = self.fileExistInDir(fileName, path)
        file_name = os.path.basename(file_path)

        #Send the length of the file name and file name
        file_name_length = str(len(file_name)).zfill(10)
        self.socket.send(file_name_length.encode())
        self.socket.send(file_name.encode())

        #Send the length of the file size and file size
        file_size = os.path.getsize(file_path)
        file_size_length = str(len(str(file_size))).zfill(10)
        self.socket.send(file_size_length.encode())
        self.socket.send(str(file_size).encode())


        with open(file_path, "rb") as file:
            data = file.read(1024)
            while data:
                self.socket.send(data)
                data = file.read(1024)
        pass

    def get():
        """
        1.         
        """
        pass

    def fileExistInDir(self, filename :str, path : str) -> str:
        directory_path = ""

        if path == "server":
            directory_path = self.server_path

        elif path == "cache":
            directory_path = self.cache_path

        elif path == "client":
            return filename
        
        else:
            sys.exit()

        absolute_dir_path = os.path.abspath(directory_path)
        file_path = os.path.join(absolute_dir_path, filename)

        if os.path.exists(file_path):
            return file_path
        
        return sys.exit()