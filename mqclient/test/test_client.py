#!/usr/bin/env python
'''
Created on 2013-4-11

@author: Wong
'''
import os,sys
sys.path.append('/Users/innerp/devplathform')
from mqclient.client import MQClient

def call_back(body,header):
    print body
    for key in header:
        print 'key:%s,value:%s'%(key,header[key])
if __name__ == '__main__':
    client = MQClient('localhost',61613,'system','manager','imtai')
    client.subscribe('/topic/foo', call_back,'mactai')
    client.start()
    pass
