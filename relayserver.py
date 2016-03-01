#!/usr/bin/env python

# Author: Mikhail Strizhov
# Date: Feb 27, 2016

import sys
import socket
import thread

NET_MSG_SIZE = 4096

def usage():
    print "Usage: ./relayserver [port]"
    sys.exit(1) 

# Purpose: create new socket
# Input: string hostname and int port number
# Output: socket or exception with error message
def createNewSocket(hostname, port):
    s = None 

    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((hostname, port)) 
	s.listen(5) 
    except socket.error, (value,message): 
        if s: 
	    s.close() 
            print "Could not open socket: " + message 
	    sys.exit(1) 
    return s 	    


# Method to handle EchoServer connection
def handleEchoServer(echosocket, relayhost, relayport):
        
    # Set params for tunnel host and port
    tunnelhost = relayhost
    tunnelport = relayport + 1;

    # Create new tunnel socket
    tunnelsocket = createNewSocket(tunnelhost, tunnelport)

    # Form message and send back to the echoserver
    tunnel_msg = tunnelhost + ":" + str(tunnelport)
    echosocket.send(tunnel_msg)
        
    # Accept connection
    tunnelclient, tunnelclientaddr = tunnelsocket.accept()

    running = 1
    while running:
	# Receive data from the tunnel client
        tunnelclientdata = tunnelclient.recv(NET_MSG_SIZE);
	if tunnelclientdata:
	    # Forward data to echo server
	    echosocket.send(tunnelclientdata)
	    # Receive replay back from echo server
	    echoserverdata  = echosocket.recv(NET_MSG_SIZE)
            if echoserverdata:
	        # Forward reply back to tunnel client
	        tunnelclient.send(echoserverdata)
	    else:
	        running = 0
	else:
	    running = 0

    tunnelsocket.close()
    echosocket.close()
    
# Method to create a new relay server
def createRelayServer(relayhost, relayport):
    relaysocket = createNewSocket(relayhost, relayport)
    
    running = 1
    while running:
        # Accept connection
        echosocket, echoaddr = relaysocket.accept()
	# Spawn a new thread for connection
        thread.start_new_thread(handleEchoServer, (echosocket, relayhost, relayport))

if __name__=='__main__':
    host = 'localhost'
    port = ''
    
    # Check command line arguments
    total = len(sys.argv)
    if total < 2:
        usage()

    port = int(sys.argv[1])
    if not port:
        usage()

    createRelayServer(host, port)
