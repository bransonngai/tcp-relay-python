# -*- coding: utf-8 -*-
"""
Created on 16/7/2022 17:42

@author: TraderB

VM: NAT Network, no script needed. call host's listen port
HOST to run this script
"""
# !/usr/bin/python

import _thread
import socket

listen_port = 3007
connect_addr = ('localhost', 8080)  # PPRO8 api port
sleep_per_byte = 0.0001


def forward(source, destination):
    source_addr = source.getpeername()
    while True:
        data = source.recv(4096)

        if data:
            destination.send(data)  # Broken pipe
        else:
            print('disconnect', source_addr)
            destination.shutdown(socket.SHUT_WR)
            break


# def forward(source, destination):
#     source_addr = source.getpeername()
#     while True:  # FIXME: error handling
#         data = source.recv(4096)  # Connection reset by peer
#         if data:
#             destination.sendall(data)  # Broken pipe
#         else:
#             print 'disconnect', source_addr
#             destination.shutdown(socket.SHUT_WR)
#             break

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('', listen_port))
serversocket.listen(5)

while True:
    (clientsocket, address) = serversocket.accept()
    print('relay accepted', address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(connect_addr)
    print('relay connected', sock.getpeername())
    _thread.start_new_thread(forward, (clientsocket, sock))
    _thread.start_new_thread(forward, (sock, clientsocket))
