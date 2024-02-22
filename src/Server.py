import socket

class UDPServer:
    def __init__(self, transmit_port, receive_port):
        self.transmit_socket = self.create_udp_socket(transmit_port)
        self.receive_socket = self.create_udp_socket(receive_port)

    def create_udp_socket(self, port):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("127.0.0.1", port))
        return udp_socket

    def transmit_message(self, message):
        self.transmit_socket.sendto(message.encode(), 7500)
        print(f"Client transmitted (sent) message '{message}' to {7500}")

    def receive_message(self, buffer_size=1024):
        data, addr = self.receive_socket.recvfrom(buffer_size)
        message = data.decode()
        print(f"Client received: {message} from {addr}")
        return message

    def close_sockets(self):
        self.transmit_socket.close()
        self.receive_socket.close()
