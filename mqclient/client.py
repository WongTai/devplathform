'''
Created on 2013-4-11

@author: Wong
'''

from mqclient.frame import ConnectFrame, MessageFrame, SubscribeFrame, SendFrame
from mqclient.mqclientscoket import MQSocket
import datetime
import logging
import os
import threading
class LoggerService():
    def __init__(self,log_level):
        user_folder = os.path.expanduser('~')
        log_folder = user_folder+'/.mqclientlog'
        #check 
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        current_time= datetime.datetime.now()
        log_filename = log_folder+'/mqclient.'+current_time.strftime('%Y-%m-%d')+'.log'
        self.log_filename =log_filename
        self.log_level = log_level
        self.init_logger()
    def init_logger(self):
        logging.basicConfig(level=self.log_level,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=self.log_filename,
                    filemode='a')
        logger = logging.getLogger()
        self.logger = logger
    def info(self,info):
        self.logger.info(info)
    def debug(self,debug):
        self.logger.debug(debug)
    def warn(self,warn):
        self.logger.warning(warn)
    def error(self,error):
        self.logger.error(error)
class MQClient(threading.Thread):
    def __init__(self,host,port,user,password):
        threading.Thread.__init__(self)
        self.logger_service = LoggerService(logging.INFO)
        self.host = host 
        self.user = user
        self.password = password
        self.port =port
        self.mqscoket = MQSocket()
    def __init_connect(self):
        self.logger_service.info('INIT SOCKET CONNECT ,host->%s,port->%s'%(self.host,str(self.port)))
        self.mqscoket.connect(self.host, self.port)
        connect_frame = ConnectFrame(self.host,self.user,self.password)
        self.mqscoket.send_message(connect_frame)
        data=self.mqscoket.receive_message(MQSocket.MESSAGE_MAX_LENGTH)
        message_frame = MessageFrame(data)
        if message_frame.get_command()!='ERROR':
            self.logger_service.info('CONNECT TO ACTIVEMQ SUCCESSFULLY ')
        else:
            self.logger_service.error(data)
    def subscribe(self,destination,client_id,call_back):
        
        self.destination = destination
        self.client_id = client_id
        self.call_back = call_back
        def should_run_func():
            subscribe_frame = SubscribeFrame(self.destination,self.client_id)
            self.mqscoket.send_message(subscribe_frame)
            running = True
            while running:
                data = self.mqscoket.receive_message(MQSocket.MESSAGE_MAX_LENGTH)
                message_frame = MessageFrame(data)
                if message_frame.get_command()!='ERROR':
                    self.call_back(message_frame.get_body(),message_frame.get_header())
                else:
                    self.logger_service.error(data)
        self.should_run_func = should_run_func
    def send(self,body,destination):
        send_frame = SendFrame(destination,body)
        self.mqscoket.send_message(send_frame)
    def run(self):
        self.__init_connect()
        self.should_run_func()
        
