import socket
import sys
import os
import time

class UDP_Transport:

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
        self.HEADERSIZE = 14
        self.LEN = 4
        pass

    def createSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def bind(self, serverIP : str, serverPort : int):
        self.socket.bind((serverIP, serverPort))
        pass

    def close(self):
        self.socket.close()
        pass

    """
    Sender is sending a file to the receiver
    @Param1: file_path, path leading to location of file being sent
    @Param2: address, return address of Receiver
    """
    def udp_put(self, file_path : str, address : socket._RetAddress):
        
        """
        Calculate file size
        Send file length (LEN:Bytes)

        while data sent != file size
            if data left >= 1000:
                send chunk of 1000 bytes
                data sent += 1000
                data left -= 1000
                wait for ACK
            else:
                send chunk of data left bytes
                data sent += data left
                data left -= data left
                wait for ACK
        
        wait for FIN 
        close UDP socket
        """

        file_size = os.path.getsize(file_path)
        file_size_length = "LEN:" + str(len(str(file_size))).zfill(10)

        self.socket.sendto(file_size_length.encode(), address)
        self.socket.sendto(file_size.encode(), address)

        with open(file_path, "rb") as file:

            data = file.read(1000)
            while data:
                """
                Send chunk
                wait for 1 second for ACK
                if data == None
                    terminate
                    print terminate message
                
                """
                self.socket.sendto(data, address)

                #figure out how to wait
                #receive ACK
                data, return_address = self.socket.recvfrom(3)

                if data:
                    data = file.read(1000)
                else:
                    print("Did not receive ACK. Terminating.")
                    sys.exit()
                

            #figure out how to wait for FIN
            data, return_address = self.socket.recvfrom(3)
            if data:
                if data.decode() == "FIN":
                    self.socket.close()
        pass

    """
    Receiver is getting a file from the Sender
    @Param1: dest_path, path where file is to be stored
    @Param2: address, return address of Sender 
    """
    def udp_get(self, dest_path : str, address : socket._RetAddress):
        """
        Receive file size (LEN:Bytes)
        while received data != file size:
            if data left >= 1000:
                data = receive 1000 bytes
                receive data += len(data)
                data left -= len(data)

                send ACK
            else:
                data = receive (data left) bytes
                receive data += len(data)
                data left -= len(data)
                
                send ACK
        """
        try:
            data, return_address = self.socket.recvfrom(self.HEADERSIZE)
            self.socket.settimeout(1)
            file_size = int(data.decode()[self.LEN - 1:])
        except self.socket.timeout:
            print("Did not receive data. Terminating.")
        finally: 
            self.socket.settimeout(None)


        received_data = 0

        with open(dest_path, "wb") as file:

            data_left = file_size
            try:
                while received_data < file_size:
                    if data_left < 1000:
                        data, return_address = self.socket.recvfrom(data_left)

                        if not data:
                            break

                        else:
                            file.write(data)
                            received_data += data_left

                            #Send ACK
                            self.socket.sendto("ACK".encode(), address)
                            self.socket.settimeout(1)

                    else:
                        data, return_address = self.socket.recvfrom(1000)
                        file.write(data)
                        received_data += len(data)
                        data_left -= len(data)

                        #Send ACK
                        self.socket.sendto("ACK".encode(), address)
                        self.socket.settimeout(1)

            except self.socket.timeout:
                print("Data transmission terminated prematurely.")    
            finally:
                self.socket.settimeout(None)
                    

        pass

