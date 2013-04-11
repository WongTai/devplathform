#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket

class MQSocket(object):

    MESSAGE_MAX_LENGTH = 4096

    def __init__(self,sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        else:
            self.sock = sock
    
    def __break_into_chunks(self,message):
        if not message:
            return []
        chunks = []
        message_length = len(message)
        if message_length<=MESSAGE_MAX_LENGTH:
            chunks.append(message)
        else:
            chunk_size =1 + message_length/MESSAGE_MAX_LENGTH
            for i in range(chunk_size):
                start = i*MESSAGE_MAX_LENGTH
                end = start + MESSAGE_MAX_LENGTH
                if end >message_length:
                    end = message_length
                chunks.append(message[start:end])
        return chunks
    def connect(self,host,port):
        self.sock.connect((host,port))

    def send_message(self,message):
        if not message:
            return
        chunks = self.__break_into_chunks(message)
        for chunk in chunks:
            self.sock.send(chunk)
    def receive_message(self,length):
        message = self.sock.recv(length)
        return message






