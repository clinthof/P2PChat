import socket as s
import threading as t

"""

Python P2P Chat with Tkinter GUI
By Felix Clinthorne and Michael James
CIS 457-30
April 23rd, 2021

Description: A peer-to-peer chat application built in Python to facilitate
communication between multiple peers simultaneously via a server.  Users
can connect to the server (in this case, set up on 127.0.0.1) and
send and/or receive messages displayed within a chat window built in Tkinter.

"""

buf_size = 4096
HOST = 'localhost'
PORT = 1024
users = []

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind((HOST, PORT))


def init_conn():
    server.listen()
    print(f'Server running\nHost: {HOST}\nPort: {PORT}')

    while True:
        try:
            client, addr = server.accept()
            users.append(client)
            server_thread = t.Thread(target=handle_conn, args=(client, addr))
            server_thread.start()
        except Exception as e:
            print(f'Error in the initial connection.  {e}')
            exit(1)


def handle_conn(client, addr):
    connected = True

    while connected:
        message = client.recv(4096)
        server_broadcast(message)

    client.close()


def server_broadcast(msg):
    for c in users:
        if c != users:
            try:
                c.send(msg)
            except Exception as e:
                print(f'Error occurred while broadcasting.  {e}')
                c.close()
                remove(c)


def remove(client):
    if client in users:
        users.remove(client)


def main():
    init_conn()


if __name__ == "__main__":
    main()
