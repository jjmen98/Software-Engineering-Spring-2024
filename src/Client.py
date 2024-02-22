import socket

def create_udp_socket(port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", port))
    return udp_socket

# Receiving Socket
client_receive_socket = create_udp_socket(7500)

# Transmitting Socket
#client_transmit_socket = create_udp_socket(7501)

try:
    while True:
        # Receive Codes up to 256 bytes
        data_receive, addr_receive = client_receive_socket.recvfrom(256)
        equipment_code = data_receive.decode()
        print(f"Client received equipment code {equipment_code} from {addr_receive}")
        
        # Transmit Response 
        #server_transmit_socket.sendto(update_message.encode(), addr_receive)
        #print(f"Server transmitted (sent) update message {update_message} to {addr_receive}")

#Close Socket 
except KeyboardInterrupt:
    client_receive_socket.close()
    #client_transmit_socket.close()
finally:
    print("Server closed.")