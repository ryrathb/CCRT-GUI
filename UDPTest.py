import socket

def udp_client(microcontroller_ip, microcontroller_port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Server address and port
    server_address = (microcontroller_ip, microcontroller_port)

    try:
        # Send data
        message = '001,1,01,01'
        print(f"Sending: {message}")
        sent = sock.sendto(message.encode(), server_address)

        # Receive response
        print("Waiting to receive...")
        data, server = sock.recvfrom(24)
        print(f"Received: {data.decode()}")

    finally:
        print("Closing socket")
        sock.close()

    

# Replace '192.168.1.XXX' with the microcontroller's IP address and adjust the port
udp_client('192.168.0.10', 8888)
