# coding:utf-8

import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''<h1>Hello, World!</h1>'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Mon,0 1 jan 2022 01:01:01 GMT',
    'Content-Type: text/html; charset=utf-8',
    f'Content-Length: {len(body.encode())}\r\n',
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    print('oh, new conn', conn, addr)
    import time
    time.sleep(30)
    request = b""
    while EOL1 and EOL2 not in request:
        request += conn.recv(1024)
    print(request)
    conn.send(response.encode())  # response转为bytes后传输
    conn.close()


def main():
    # socket.AF_INET用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM用于基于TCP的流式socket通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用，保证我们每次按Ctrl+C组合键后，快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    serversocket.listen(5)  # 设置backlog-socket连接最大排队数量
    print('http://127.0.0.1:8000')

    try:
        while True:
            conn, address = serversocket.accept()
            handle_connection(conn, address)
    finally:
        serversocket.close()


if __name__ == '__main__':
    main()
