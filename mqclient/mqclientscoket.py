#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2013-4-11

@author: Wong
'''

import socket

class MQSocket(object):

    MESSAGE_MAX_LENGTH = 4096

    def __init__(self,sock=None,blocking=True):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.setblocking(blocking)
        else:
            self.sock = sock
    
    def __break_into_chunks(self,message):
        if not message:
            return []
        chunks = []
        message_length = len(message)
        if message_length<=MQSocket.MESSAGE_MAX_LENGTH:
            chunks.append(message)
        else:
            chunk_size =1 + message_length/MQSocket.MESSAGE_MAX_LENGTH
            for i in range(chunk_size):
                start = i*MQSocket.MESSAGE_MAX_LENGTH
                end = start + MQSocket.MESSAGE_MAX_LENGTH
                if end >message_length:
                    end = message_length
                chunks.append(message[start:end])
        return chunks
    def connect(self,host,port):
        self.sock.connect((host,port))

    def send_message(self,frame):
        message = frame.frame_to_str()
        print message
        if not message:
            return
        chunks = self.__break_into_chunks(message)
        for chunk in chunks:
            sended_length = self.sock.send(chunk)
            if sended_length == 0:
                raise RuntimeError("socket connection broken")
    def receive_message(self,length):
        message = self.sock.recv(length)
        return message
    def close(self):
        self.sock.close()
