'''
Created on 2013-4-11

@author: Wong
'''
#!/usr/bin/env python
# -*- coding:utf-8
from mqclient.frame import ConnectFrame, MessageFrame, SubscribeFrame
from mqclient.mqclientscoket import MQSocket
import socket
if __name__=='__main__':
    print 'RECEIVER'
    HOST = 'localhost'    # The remote host
    PORT = 61613             # The same port as used by the server
    mqsocket = MQSocket()
    mqsocket.connect(HOST, PORT)
    connect_frame = ConnectFrame(HOST,login='system',password='manager')
    mqsocket.send_message(connect_frame)
    data = mqsocket.receive_message(MQSocket.MESSAGE_MAX_LENGTH)
    message_frame = MessageFrame(data)
    print message_frame.get_command()
    header = message_frame.get_header()
    for key in header:
        print 'key:%s,value:%s'%(key,header[key])
    print message_frame.get_body()
    subscribe_frame = SubscribeFrame('/queue/foo','tai')
    mqsocket.send_message(subscribe_frame)
    while 1:
        data = mqsocket.receive_message(MQSocket.MESSAGE_MAX_LENGTH)
        message_frame = MessageFrame(data)
        print message_frame.get_command()
        header = message_frame.get_header()
        for key in header:
            print 'key:%s,value:%s'%(key,header[key])
        print message_frame.get_body()
    mqsocket.close()
    #print 'Received\n', repr(data)
