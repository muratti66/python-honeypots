import socket
import sys
from _thread import *

import time

from library import id_generate

host = None
port = None
log_th = None
conf_th = None
header_th = None
command_w_th = None


class TelnetServer:

    def __init__(self):
        global host, port, log_th, conf_th, header_th, command_w_th, MENU_MESSAGE
        self.host = host
        self.port = port
        self.conf_th_ic = conf_th
        self.header_th_ic = header_th
        self.command_w_th_inc = command_w_th
        self.log_th = log_th
        self.hostname = conf_th.get_item(q_key='general').get('hostname')
        self.telnet_queue_size = int(conf_th.get_item(q_key='general').get('telnet_queue_size'))
        self.telnet_message_path = conf_th.get_item(q_key='general').get('telnet_message_path')
        self.telnet_recv_size = int(conf_th.get_item(q_key='general').get('telnet_recv_size'))
        self.sleep_between = int(conf_th.get_item(q_key='general').get('sleep_between'))
        self.no_answer = int(conf_th.get_item(q_key='general').get('no_answer'))

    def recv_message(self, conn):
        bytes_received = conn.recv(self.telnet_recv_size)
        received = bytes.decode(bytes_received).strip()
        return received.encode('ascii', 'ignore').decode()

    def send_message(self, conn, message, dis_newline):
        if dis_newline:
            message = message + "\n"
        conn.send(bytes(message.encode()))

    def login_interface(self, conn, id, client_ip, client_port):
        message = "Username: "
        self.send_message(conn=conn, message=message, dis_newline=False)
        self.command_w_th_inc.write_commands(data=message, qid=id)
        username = self.recv_message(conn)
        commands = "Client {}, username '{}' entered".format(client_ip, username)
        self.command_w_th_inc.write_commands(data=commands, qid=id)
        self.log_th.log_info('{} - {}:{} client username entered : {} '.format(
            id, client_ip, client_port, username))
        message = "Password: "
        self.send_message(conn=conn, message=message, dis_newline=False)
        self.command_w_th_inc.write_commands(data=message, qid=id)
        password = self.recv_message(conn)
        commands = "Client {}, password '{}' entered".format(client_ip, password)
        self.command_w_th_inc.write_commands(data=commands, qid=id)
        self.log_th.log_info('{} - {}:{} client password entered : {} '.format(
            id, client_ip, client_port, password))
        message = "OK"
        self.send_message(conn=conn, message=message, dis_newline=True)
        self.command_w_th_inc.write_commands(data=message, qid=id)

    def telnet_thread(self, conn, addr):
        id = id_generate(size=16)
        client_ip = addr[0]
        client_port = str(addr[1])
        self.log_th.log_info('{}:{} connected to proxy socket'.format(client_ip, client_port))
        commands = "Client : " + client_ip + ":" + client_port + " is connected to telnet://" \
                   + self.hostname + ":" + str(self.port)
        self.command_w_th_inc.write_commands(data=commands, qid=id)
        self.login_interface(conn=conn, id=id, client_ip=client_ip, client_port=client_port)
        header_th.write_header(ip=client_ip, qid=id)
        if self.no_answer != 0:
            while True:
                self.recv_message(conn)

        empty_try = 0
        while True:
            msg = self.telnet_message_path + '>'
            self.send_message(conn=conn, message=msg, dis_newline=False)
            self.command_w_th_inc.write_commands(data=msg, qid=id)
            if self.sleep_between != 0:
                time.sleep(self.sleep_between)

            command = self.recv_message(conn)
            if command == "":
                if empty_try > 5:
                    break
                else:
                    empty_try += 1
            commands = "Client {}, command '{}' entered".format(client_ip, command)
            self.command_w_th_inc.write_commands(data=commands, qid=id)
            self.log_th.log_info('{} - {}:{} client command entered : {} '.format(
                id, client_ip, client_port, command))
            if command == 'logout':
                break
            else:
                self.send_message(conn=conn, message="ERROR : Unrecognized command", dis_newline=True)

        self.log_th.log_info('{}:{} disconnected'.format(client_ip, client_port))
        commands = "Client : " + client_ip + ":" + client_port + " is disconnected"
        self.command_w_th_inc.write_commands(data=commands, qid=id)
        conn.shutdown(socket.SHUT_RD)
        conn.close()


def start_operation():
    telnet_queue_size = int(conf_th.get_item(q_key='general').get('telnet_queue_size'))
    telnet_recv_size = int(conf_th.get_item(q_key='general').get('telnet_recv_size'))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(telnet_recv_size)
        log_th.log_info('{}:{} socket started..'.format(host, str(port)))
    except socket.error as message:
        if s:
            s.shutdown()
            s.close()
            log_th.log_error("Could not open socket:", message)
        sys.exit(1)

    while 1:
        conn, client_addr = s.accept()
        start_new_thread(TelnetServer().telnet_thread, (conn, client_addr))


def server_init(log_set, conf_set, header_set, commands_w_set):
    global log_th, conf_th, header_th, command_w_th, host, port
    log_th = log_set
    conf_th = conf_set
    header_th = header_set
    command_w_th = commands_w_set
    host = conf_set.get_item(q_key='general').get('sock_ip')
    port = int(conf_set.get_item(q_key='general').get('port'))
