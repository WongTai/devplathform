#coding:utf-8
'''
Created on 2013-4-11

@author: Wong
'''
class BaseFrame:
    def frame_to_str(self):
        raise NotImplementedError( "abstract method -- subclass %s must override" % self.__class__ )
    @classmethod
    def init_connect_header(cls,host,login=None,password=None,client_id=None):
        header = {}
        header['accept-version'] = '1.1,1.2'
        header['host'] = host
        if client_id:
            header['client-id']=client_id
        if login:
            header['login'] = login
        if password:
            header['passcode'] = password
        return header
    @classmethod
    def init_send_header(cls,destination,content_type,content_length=0):
        header = {}
        header['destination'] = destination
        header['content-type'] = content_type
        if content_length:
            header['content-length'] = content_length
        return header
    @classmethod
    def init_subscribe_header(cls,destination,subscribe_name=None,ack='auto'):
        header = {}
        header['destination'] = destination
        if subscribe_name:
            header['activemq.subscriptionName'] = subscribe_name
        header['ack'] = ack
        return header
    @classmethod
    def init_unsubscribe_header(cls,client_id):
        header={}
        header['id'] = client_id
        return header
    @classmethod
    def init_ack_header(cls,client_id,transaction=None):
        header = {}
        header['id'] = client_id
        if transaction:
            header['transaction'] = transaction
        return header
    @classmethod
    def init_disconnect(cls,receipt):
        header={}
        header['receipt'] = receipt
        return header
class ConnectFrame(BaseFrame):
    def __init__(self,host,login=None,password=None,client_id=None):
        self.header = BaseFrame.init_connect_header(host,login,password,client_id)
    def frame_to_str(self):
        frame_content_list = []
        command = 'CONNECT'
        frame_content_list.append(command)
        frame_content_list.append('\n')
        for key in self.header.keys():
            frame_content_list.append(key)
            frame_content_list.append(':')
            frame_content_list.append(str(self.header[key]))
            frame_content_list.append('\n')
        frame_content_list.append('\n')
        frame_content_list.append('\x00')
        return ''.join(frame_content_list)
class SubscribeFrame(BaseFrame):
    def __init__(self,destination,subscribe_name=None,ack='auto'):
        self.header = BaseFrame.init_subscribe_header(destination,subscribe_name,ack)
    def frame_to_str(self):
        command ='SUBSCRIBE'
        frame_content_list = []
        frame_content_list.append(command)
        frame_content_list.append('\n')
        for key in self.header.keys():
            frame_content_list.append(key)
            frame_content_list.append(':')
            frame_content_list.append(str(self.header[key]))
            frame_content_list.append('\n')
        frame_content_list.append('\n')
        frame_content_list.append('\x00')
        return ''.join(frame_content_list)
class UnSubscibeFrame(BaseFrame):
    def __init__(self,client_id):
        self.header = BaseFrame.init_unsubscribe_header(client_id)
    def frame_to_str(self):
        command = 'UNSUBSCRIBE'
        frame_content_list = []
        frame_content_list.append(command)
        frame_content_list.append('\n')
        for key in self.header.keys():
            frame_content_list.append(key)
            frame_content_list.append(':')
            frame_content_list.append(str(self.header[key]))
            frame_content_list.append('\n')
        frame_content_list.append('\n')
        frame_content_list.append('\x00')
        return ''.join(frame_content_list)
class SendFrame(BaseFrame):
    def __init__(self,destination,body,content_type='text/palin'):
        content_length = 0
        if body:
            content_length = len(body)
        self.body = body
        self.header = BaseFrame.init_send_header(destination, content_type, content_length)
    def frame_to_str(self):
        command = 'SEND'
        frame_content_list = []
        frame_content_list.append(command)
        frame_content_list.append('\n')
        for key in self.header.keys():
            frame_content_list.append(key)
            frame_content_list.append(':')
            frame_content_list.append(str(self.header[key]))
            frame_content_list.append('\n')
        frame_content_list.append('\n')
        frame_content_list.append(self.body)
        frame_content_list.append('\x00')
        return ''.join(frame_content_list)
class DisconnectFrame(BaseFrame):
    def __init__(self,receipt):
        self.header = BaseFrame.init_disconnect(receipt)
    def frame_to_str(self):
        command = 'DISCONNECT'
        frame_content_list = []
        frame_content_list.append(command)
        frame_content_list.append('\n')
        for key in self.header.keys():
            frame_content_list.append(key)
            frame_content_list.append(':')
            frame_content_list.append(str(self.header[key]))
            frame_content_list.append('\n')
        frame_content_list.append('\n')
        frame_content_list.append('\x00')
        return ''.join(frame_content_list)
class MessageFrame(BaseFrame):
    """
        用于解析来自server 的frame 包含如下frame:
    1, CONNECTED 和服务器成功建立链接回复
    2，MESSAGE 服务器向客户端推送的消息
    3，ERROR 服务器返回的错误信息
    4，RECEIPT 关闭服务器链接时返回完全接受了客户端消息的回应
    """
    def __init__(self,message):
        parser = ActiveMQFrameParser(message)
        self.command,self.header,self.body =parser.parse() 
    def is_error(self):
        if self.command =='ERROR':
            return False
        else:
            return True
    def get_body(self):
        return self.body
    def get_command(self):
        return self.command
    def get_header(self):
        return self.header
class FrameParser(object):
    def __init__(self,message):
        self.message = message
    def validate_message(self):
        raise NotImplementedError( "abstract method -- subclass %s must override" % self.__class__ )
    def parse(self):
        raise NotImplementedError( "abstract method -- subclass %s must override" % self.__class__ )
class ActiveMQFrameParser(FrameParser):
    def __init__(self,message):
        FrameParser.__init__(self, message)
    def validate_message(self):
        activemq_endflag = '\x00\n'
        other_endflag = '\x00'
        is_activemq = self.message.endswith(activemq_endflag)
        is_other = self.message.endswith(other_endflag)
        if is_activemq or is_other:
            self.message = self.message.replace(activemq_endflag,'')
            self.message = self.message.replace(other_endflag,'')
            return True
        return False
    def parse(self):
        if not self.validate_message():
            return '',{},''
        #找出第一处出现两个换行符的位置及 body起始位置
        body_index_start = self.message.find('\n\n')
        part1 = self.message[0:body_index_start].strip()
        part2 = self.message[body_index_start:]
        part1_list = part1.split('\n')
        command = ''
        header = {}
        for part in part1_list:
            if part:
                if part.find(':')==-1:
                    command = part
                else:
                    #AactiveMQ session格式
                    #session:ID:xxxxx:xx
                    if part.startswith('session'):
                        seperate = part.find(':')
                        k = part[0:seperate]
                        v = part[seperate+1:]
                    else:
                        kv = part.split(':')
                        k = kv[0]
                        v = kv[1]
                    header[k] = v
        return command,header,part2[2:]
