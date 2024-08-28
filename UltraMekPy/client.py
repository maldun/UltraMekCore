import socket

PORT = 8563
IP = "127.0.0.1"
BUFFER_SIZE = 1024

class UDPClient:
    def __init__(self,port=PORT,ip=IP,standard_buffer_size=BUFFER_SIZE):
        self.port = port
        self.ip = ip
        self.standard_buffer_size = standard_buffer_size
        self.create_socket()

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self,msg):
        self.socket.sendto(msg.encode(), (self.ip, self.port))

    def recieve(self,buffer_size=None,return_port_info=False):
        if buffer_size is None:
            buffer_size = self.standard_buffer_size
        data, (recv_ip, recv_port) = self.socket.recvfrom(buffer_size)
        if return_port_info is True:
            return data, (recv_ip, recv_port)
        else:
            return data
        


