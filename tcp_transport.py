from io import BufferedReader
import socket

class TCP_Transport:

    def __init__(self, serverIP : str, serverPort : int, cacheIP : str, cachePort : int) -> None:
        self.__serverIP = serverIP
        self.__serverPort = serverPort
        self.__cacheIP = cacheIP
        self.__cachePort = cachePort
        pass

    """
    Client connects to the server and attemps to upload a file
    @Param: file : BufferedReader
    """
    def clientPutTCP(self, file : BufferedReader) -> None:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.__serverIP,self.__serverPort))
            data = file.read(1024)
            sock.sendfile(data)
        return