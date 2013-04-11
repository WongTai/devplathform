'''
Created on 2013-4-11

@author: Wong
'''
from mqclient.client import MQClient

def call_bakc(body,header):
    print body
    for key in header:
        print 'key:%s,value:%s'%(key,header[key])
if __name__ == '__main__':
    client = MQClient('localhost',61613,'system','manager')
    client.subscribe('/topic/foo', 'mqclient', call_bakc)
    client.start()
    pass