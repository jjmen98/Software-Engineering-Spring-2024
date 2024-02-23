import socket

class UDPServer:
    def __init__(self, transmit_port, receive_port):
        self.transmit_socket = self.create_udp_socket(transmit_port)
        # allow broadcasting of messages through transmit socket
        self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.receive_socket = self.create_udp_socket(receive_port)
        print("UDP Server Up")

    def create_udp_socket(self, port):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(("127.0.0.1", port))
        return udp_socket

    def transmit_message(self, message):
        self.transmit_socket.sendto(message.encode(), ('127.0.0.1', 7500))
        print(f"Server transmitted (sent) message '{message}' to {7500}")

    def receive_message(self, buffer_size=1024):
        data, addr = self.receive_socket.recvfrom(buffer_size)
        message = data.decode()
        print(f"Server received: {message} from {addr}")
        return message

    def close_sockets(self):
        self.transmit_socket.close()
        self.receive_socket.close()