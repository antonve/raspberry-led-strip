#!/usr/bin/env python

import led_driver
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Turns a list into a list of lists where the nested lists have length n
# see http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-eve
nly-sized-chunks-in-python
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def write_to_led_strip(data):
    if(len(data) >= 60):
        try:
            toWrite = [[int(elem[0:2], 16), int(elem[2:4], 16), int(elem[4:6], 16)] for elem in list(chunks(data, 6))]
            print "sending to LED strip %s" % toWrite
            led_driver.write_colors(toWrite)
            return list
        except ValueError, e:
            return []
    else:
         print "not enough characters"

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(60)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
                write_to_led_strip(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()


