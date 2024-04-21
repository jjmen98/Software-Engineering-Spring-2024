import socket


class UDPServer:
    # ports are (IP, port) tuple format, defaults to local ports 7500 for transmit and 7501 for receive
    def __init__(self, transmit_port=('127.0.0.1', 7500), receive_port=('127.0.0.1', 7501)):
        self.transmit_port = transmit_port
        self.receive_port = receive_port
        self.receive_socket = self.create_udp_socket(self.receive_port)
        print("UDP Server Up")

    def create_udp_socket(self, port):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(port)
        return udp_socket

    def transmit_message(self, message):
        self.receive_socket.sendto(message.encode(), self.transmit_port)
        print(f"Server transmitted (sent) message '{message}' to {7500}")

    def receive_message(self, buffer_size=1024):
        data, addr = self.receive_socket.recvfrom(buffer_size)
        message = data.decode()
        print(f"Server received: {message} from {addr}")
        return message

    def close_sockets(self):
        self.receive_socket.close()
