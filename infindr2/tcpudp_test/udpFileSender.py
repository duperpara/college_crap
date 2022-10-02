# ----- sender.py ------

# !/usr/bin/env python

from socket import *
import sys
import hashlib


def get_digest(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def run():

    s = socket(AF_INET, SOCK_DGRAM)
    host = sys.argv[1]
    port = int(sys.argv[2])
    buf = 1024
    addr = (host, port)

    file_name = sys.argv[3]
    # file_name = b"imagem.jpg"
    print()
    f = open(file_name, "rb")

    print("Sending: " + file_name)
    s.sendto(file_name.encode('utf-8'), addr)
    print("Waiting for confirmation to send data...")
    resposta = s.recvfrom(1024)
    print(str(resposta[0].decode('utf-8')))
    print("Sending data...")
    data = f.read(buf)
    while (data):
        if (s.sendto(data, addr)):
            data = f.read(buf)

    s.sendto(b"\r", addr)
    resposta = s.recvfrom(1024)
    print(str(resposta[0].decode('utf-8')))
    s.close()
    f.close()


if __name__ == '__main__':
    run()
