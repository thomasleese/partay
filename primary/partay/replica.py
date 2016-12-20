import socket


class Replica:

    def __init__(self, address, port=1234):
        self.address = (address, port)

    def send(self, payload):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.address)
            s.sendall(payload)
