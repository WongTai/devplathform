#!/usr/bin/env python
# -*- coding:utf-8
import socket
if __name__=='__main__':
    HOST = 'localhost'    # The remote host
    PORT = 61613             # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('CONNECT\nlogin:system\npasscode:manager\nclient-id:ztai\n\n\x00' )
    data = s.recv(4096)
    print repr(data)
    s.sendall('SEND\ndestination:/queue/foo\ncontent-type:text/plain\n hello world\n\n\x00' ) 
    while 1:
        data = s.recv(4096)
        print repr(data)
    s.close()
    #print 'Received\n', repr(data)







