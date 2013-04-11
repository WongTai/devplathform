#coding:utf-8

class BaseFrame:

    @classmethod
    def init_connect_header(cls,host,login=None,password=None):
        header = {}
        header['accept-version'] = '1.1,1.2'
        header['host'] = host
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
    def init_subscribe_header(cls,destination,client_id,ack='auto'):
        header = {}
        header['destination'] = destination
        header['id']= client_id
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
class ConnectFrame(BaseFrame):
    def __init__(self,host,login=None,password=None):
        self.header = BaseFrame.init_connect_header(host,login,password)
    def frame_to_str(self):
        frame_content_list = []
        command = 'CONNECT'
        frame_content_list.append(command).append('\n')
        for key in self.header.keys():
            frame_content_list.append(key).append(':').append(str(self.header[key])).append('\n')
        frame_content_list.append('\n')
        frame_content_list.append('\x00')
        return ''.join(frame_content_list)
class SubscribeFrame(BaseFrame):
    def __init__(self,destination,client_id,ack='auto'):
        self.header = BaseFrame.init_subscribe_header(destination,client_id,ack)
    def frame_to_str(self):
        command ='SUBSCRIBE'
        frame_content_list = []
        frame_content_list.append(command).append('\n')
        for key in self.header.keys():
            frame_content_list.append(key).append(':').append(str(self.header[key])).append('\n')
        frame_content_list.append('\n')
        frame_content_list.append('\x00')
        return ''.join(frame_content_list)
class MessageFrame(BaseFrame):
    
    def __init__(self,message):
        parser = FrameParser(message)
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
        if self.endswith('\x00') or self.endswith('\x00\n'):
            return True
        return False
    def parse(self):
        if not self.validate_message():
            return '',{},''
        #\n\n是body开始位置
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
                    kv = part.split(':')
                    header[kv[0]] = kv[1]
        return command,header,part2

            
            




        




