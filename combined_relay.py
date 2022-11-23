# -*- coding: utf-8 -*-
"""
Created on 16/7/2022 17:42

@author: TraderB

VM: NAT Network, no script needed. call host's listen port
HOST to run this script

udprelay.cpython-38.pyc 8080:192.168.2.149:3008
"""
# !/usr/bin/python
import sys
import _thread
import socket
from threading import Thread
from time import sleep


listen_port = 3007
connect_addr = ('localhost', 8080)  # PPRO8 api port
sleep_per_byte = 0.0001
udp_remote_host = ''
udp_remote_port = 3008
udp_local_port = 8080
udp_uri = f'local'


def start_tcp():

    def forward(source, destination):
        source_addr = source.getpeername()
        while True:
            try:
                data = source.recv(4096)
            except ConnectionResetError as e:
                break
                print(str(e))

            if data:
                try:
                    destination.send(data)  # Broken pipe
                except Exception as e:
                    print(str(e))
                    pass
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
        # address is a tuple
        ip = address[1]
        global udp_remote_host
        if not udp_remote_host:
            print('update udp_remote_host')
            udp_remote_host = ip
        else:
            print(f'remote ip is : {udp_remote_host}')
        print('relay accepted', address)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(connect_addr)
        print('relay connected', sock.getpeername())
        _thread.start_new_thread(forward, (clientsocket, sock))
        _thread.start_new_thread(forward, (sock, clientsocket))

def start_udp():

    # Whether or not to print the IP address and port of each packet received
    debug = True

    def fail(reason):
        sys.stderr.write(reason + '\n')
        sys.exit(1)
    #
    # if len(sys.argv) != 2 or len(sys.argv[1].split(':')) != 3:
    #     fail('Usage: udp-relay.py localPort:remoteHost:remotePort')

    localPort = udp_remote_host
    remoteHost = udp_remote_host
    remotePort = udp_remote_port

    try:
        localPort = int(localPort)
    except:
        fail('Invalid port number: ' + str(localPort))
    try:
        remotePort = int(remotePort)
    except:
        fail('Invalid port number: ' + str(remotePort))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', localPort))
    except:
        fail('Failed to bind on port ' + str(localPort))

    knownClient = None
    knownServer = (remoteHost, remotePort)
    sys.stdout.write('All set, listening on ' + str(localPort) + '.\n')
    while True:

        while True:
            if udp_remote_host:
                try:
                    data, addr = s.recvfrom(32768)
                except ConnectionResetError:
                    if debug:
                        print('Ubuntu reset ? no problem, udp dont give a shit, just try again')
                        break

                if knownClient is None or addr != knownServer:
                    if debug:
                        print("")
                    knownClient = addr

                if debug:
                    print("Packet received from " + str(addr))

                if addr == knownClient:
                    if debug:
                        print("\tforwarding to " + str(knownServer))

                    s.sendto(data, knownServer)
                else:
                    if debug:
                        print("\tforwarding to " + str(knownClient))
                    s.sendto(data, knownClient)


if __name__ == '__main__':
    print('start TCP relay')
    t = Thread(target=start_tcp)
    t.start()

    sleep(3)
    print('start UDP relay')