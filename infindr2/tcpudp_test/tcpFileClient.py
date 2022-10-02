import socket                   # Import socket module
import hashlib
import sys
import os


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


print('started')

s = socket.socket()             # Create a socket object
host = sys.argv[1]
port = int(sys.argv[2])                    # Reserve a port for your service.

s.connect((host, port))

file_name = sys.argv[3].encode('utf-8')
s.send(file_name)
file_name = "downloaded_" + file_name.decode('utf-8')
file_name = file_name.encode('utf-8')

with open(file_name, 'wb') as f:
    print('file opened')
    while True:
        data = s.recv(1024)
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
print(get_digest(file_name))
