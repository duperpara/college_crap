import os
import socket
import hashlib
import pandas as pd
from time import sleep


def udp_up(host, port, file):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(5)
        with open(file, 'rb') as f:
            send_file_name = os.path.basename(file)
            s.sendto(send_file_name.encode('utf-8'), (host, port))
            res = s.recvfrom(1024)
            data = f.read(1024)
            while data:
                if s.sendto(data, (host, port)):
                    data = f.read(1024)
            s.sendto(b'\r', (host, port))
            # res = s.recvfrom(1024)
    return get_digest(file)


def tcp_get_hash(host, port, file):
    with socket.socket() as s:
        s.settimeout(5)
        s.connect((host, port))
        hash_file_name = os.path.basename(file)[:-4] + '_hash.txt'
        s.send(hash_file_name.encode('utf-8'))
        data = bytearray(b'')
        while True:
            dat = s.recv(1024)
            if not dat:
                break
            data += dat
    return data.decode('utf-8')


def tcp_down(host, port, file, out_path, prefix):
    with socket.socket() as s:
        s.settimeout(5)
        s.connect((host, port))
        s.send(os.path.basename(file).encode('utf-8'))
        sufix_file_name = prefix + os.path.basename(file)
        with open(os.path.join(out_path, sufix_file_name), 'wb') as f:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
    return get_digest(os.path.join(out_path, sufix_file_name))


def run(in_path, file_names, out_path, host, tcp_port, udp_port, qt_itr: int):
    hash_di = {}
    for file_name in file_names:
        hash_di[file_name] = []
        for itr in range(0, qt_itr):
            os.system('cls')
            print(f'{file_name} {itr+1}/{qt_itr}')
            local_hash = udp_up(host, udp_port, os.path.join(
                in_path, file_name))
            server_hash = tcp_get_hash(host, tcp_port, file_name)
            download_hash = tcp_down(
                host, tcp_port, os.path.join(out_path, file_name), out_path, prefix=str(itr))
            hash_di[file_name].append((str(itr) + file_name, local_hash, server_hash, download_hash))

    return hash_di

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


if __name__ == '__main__':
    resources_path = r'C:\Users\luiz\PycharmProjects\college_crap\infindr2\tcpudp_test\resources'
    output_path = r'C:\Users\luiz\PycharmProjects\college_crap\infindr2\tcpudp_test\output'

    host = '200.135.184.51'
    tcp_port = 8883
    udp_port = 8000

    data = run(resources_path, resouce_files, output_path, host, tcp_port, udp_port, qt_itr=100)
    for name, file_data in data.items():
        df = pd.DataFrame(file_data, columns=['file_name', 'local_hash', 'server_hash', 'download_hash'])
        df.to_csv(os.path.join(output_path, f'{name}_resultados.csv'))
