import socket
from select import select

tasks = []
to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 18000))
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()  # read
        print('connection from', addr)
        client(client_socket)


def client(client_socket):
    while True:
        yield ('read', client_socket)
        print('before client_socket_recv')
        request = client_socket.recv(4096)  # read
        print('after client_socket_recv')
        if not request:
            print('before break client: not request')
            break
        else:
            response = 'Hello\n'.encode()
            yield ('write', client_socket)
            client_socket.send(response)  # write

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            reason, sock = next(task)
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except:
            pass


tasks.append(server())
