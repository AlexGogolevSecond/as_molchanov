import selectors
import socket
from datetime import datetime


selector = selectors.DefaultSelector()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 18000))
    server_socket.listen()

    selector.register(fileobj=server_socket,events=selectors.EVENT_READ, data=accept_connection)
    print(datetime.now(), ': зарегили серверный сокет и передали в selector его и метод accept_connection')

def accept_connection(server_socket):
    print(datetime.now(), ': вошли в метод accept_connection')
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)
    print(datetime.now(), ': зарегили клиентский сокет и передали в selector его и метод send_message')

def send_message(client_socket):
    print(datetime.now(), ': вошли в метод send_message')
    request = client_socket.recv(4096)
    if request:
        client_socket.send(f'{request} 123\n'.encode())
    else:
        selector.unregister(client_socket)
        client_socket.close()

def event_loop():
    while True:
        # нужно получить выборку объектов, которые готовы для чтения или для записи
        print(datetime.now(), ': в методе event_loop, перед selector.select()')
        keys_events = selector.select()  # [(key, events),...]
        print(datetime.now(), ': в методе event_loop, перед циклом')
        for key, _ in keys_events:
            print(datetime.now(), ': в цикле; key.data:', key.data)
            print(datetime.now(), ': в цикле; key.fileobj:', key.fileobj)
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    print(datetime.now(), ': в методе main() после server() перед event_loop()')
    event_loop()