# coding:utf-8

import errno
import socket
import threading
import time

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''<h1>Hello, world!</h1> - from {thread_name}'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Mon, 01 jan 2022 01:01:01 GMT'
    'Content-Type: text/plain; charset=utf-8',
    'Content_Length: {length}\r\n',
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    # print(conn, addr)
    # time.sleep(60)            # 可以自行尝试打开注释，设置睡眠时间
    request = b""
    while EOL1 and EOL2 not in request:
        request += conn.recv(1024)      # 注意设置为非阻塞模式这里会报错，建议搜索一下问题来源

    print(request)
    current_thread = threading.currentThread()
    content_length = len(body.format(thread_name=current_thread.name).encode())
    print(current_thread.name)
    conn.send(response.format(thread_name=current_thread.name,
                              length = content_length).encode())
    conn.close()


def main():
    # socket.AF_INET用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM用于基于TCP的流式socket通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用，保证我们每次按Ctrl+C组合键之后，快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    # 可参考：https://stackoverflow.com/questions/2444459/python-sock-listen
    serversocket.listen(10)
    print('http://127.0.0.1:8000')
    serversocket.setblocking(0)     # 设置socket为非阻塞模式

    try:
        i = 0
        while True:
            try:
                conn, address = serversocket.accept()
            except socket.error as e:
                if e.args[0] != errno.EAGAIN:
                    raise
                continue
            i += 1
            print(i)
            t = threading.Thread(target=handle_connection, args=(conn, address),
                                 name = 'thread-%s' % i)
            t.start()
    finally:
        serversocket.close()


if __name__ == '__main__':
    main()
