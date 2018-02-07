import socket, sys
import _thread as thread

import time

from library import id_generate


class FTPServer:

    def __init__(self):
        global host, port, log_th, conf_th, header_th, command_w_th, data_w_th
        self.conn = None
        self.addr = None
        self.rest = False
        self.pasv_mode = False
        self.id = None
        self.host = host
        self.port = port
        self.client_ip = None
        self.client_port = None
        self.conf_th_ic = conf_th
        self.header_th_ic = header_th
        self.command_w_th_inc = command_w_th
        self.data_w_th_inc = data_w_th
        self.log_th = log_th
        self.hostname = conf_th.get_item(q_key='general').get('hostname')
        self.std_recv_size = int(conf_th.get_item(q_key='general').get('std_recv_size'))
        self.data_recv_size = int(conf_th.get_item(q_key='general').get('data_recv_size'))
        self.message_welcome = conf_th.get_item(q_key='messages').get('welcome')
        self.sleep_between = int(conf_th.get_item(q_key='general').get('sleep_between'))
        self.no_answer = int(conf_th.get_item(q_key='general').get('no_answer'))

    def send_byte(self, message):
        re_format = message + '\r\n'
        self.conn.send(re_format.encode())
        self.command_w_th_inc.write_commands(data=message, qid=self.id)

    def recv_byte(self, conn, ip):
        try:
            bytes_received = conn.recv(int(self.std_recv_size))
            try:
                received = bytes.decode(bytes_received).strip()
            except:
                received = bytes_received.strip()
            commands = received
            self.command_w_th_inc.write_commands(data=commands, qid=self.id)
            return received.encode('ascii', 'ignore').decode()
        except:
            return ''

    def ftp_thread(self, conn, client_addr):
        self.id = id_generate(size=16)
        self.conn = conn
        self.addn = client_addr
        self.client_ip = client_addr[0]
        self.client_port = str(client_addr[1])
        self.log_th.log_info('{}:{} connected to ftp socket'.format(self.client_ip, self.client_port))
        commands = "Client : " + self.client_ip + ":" + self.client_port + " is connected to ftp://" \
                   + self.hostname + ":" + str(self.port)
        self.command_w_th_inc.write_commands(data=commands, qid=self.id)
        header_th.write_header(ip=self.client_ip, qid=self.id)
        if self.no_answer != 0:
            while True:
                self.recv_byte(conn, ip=self.client_ip)

        self.send_byte(self.message_welcome)
        while True:
            if self.sleep_between != 0:
                time.sleep(self.sleep_between)
            cmd = self.recv_byte(conn, ip=self.client_ip)
            if not cmd:
                break
            else:
                try:
                    func = getattr(self, cmd[:4].strip().upper())
                    func(cmd)
                except Exception as e:
                    self.log_th.log_error(e)
                    self.send_byte('500 Sorry.')
        commands = "Client : " + self.client_ip + ":" + self.client_port + " is disconnected from ftp://" \
                   + self.hostname + ":" + str(self.port)
        self.command_w_th_inc.write_commands(data=commands, qid=self.id)
        self.log_th.log_info('{}:{} disconnected from ftp socket'.format(self.client_ip, self.client_port))

    def SYST(self, cmd):
        self.send_byte('215 UNIX Type: L8')

    def OPTS(self, cmd):
        if cmd[5:-2].upper() == 'UTF8 ON':
            self.send_byte('200 OK.')
        else:
            self.send_byte('451 Sorry.')

    def USER(self, cmd):
        self.send_byte('331 OK.')

    def PASS(self, cmd):
        self.send_byte('230 OK.')

    def QUIT(self, cmd):
        self.send_byte('221 Goodbye.')
        self.conn.shutdown(socket.SHUT_WR)
        self.conn.close()

    def NOOP(self, cmd):
        self.send_byte('200 OK.')

    def TYPE(self, cmd):
        self.mode = cmd[5]
        self.send_byte('200 Binary mode.')

    def CDUP(self, cmd):
        self.send_byte('200 OK.')

    def PWD(self, cmd):
        cwd = '/'
        msg = '257 \"' + cwd + '\"'
        self.send_byte(msg)

    def NLST(self, cmd):
        self.send_byte('150 Here comes the directory listing.')
        self.start_datasock()
        self.datasock.send('\r\n'.encode())
        self.stop_datasock()
        self.send_byte('226 Directory send OK.')

    def CWD(self, cmd):
        self.send_byte('250 OK.')

    def PORT(self, cmd):
        if self.pasv_mode:
            self.servsock.close()
            self.pasv_mode = False
        l = cmd[5:].split(',')
        self.dataAddr = '.'.join(l[:4])
        self.dataPort = (int(l[4]) << 8) + int(l[5])
        self.send_byte('200 Get port.')

    def PASV(self, cmd):
        self.pasv_mode = True
        self.servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servsock.bind((self.host, 0))
        self.servsock.listen(1)
        ip, port = self.servsock.getsockname()
        self.log_th.log_info('Changed mod, ip: ' + ip + ', port : ' + str(port))
        msg = '227 Entering Passive Mode (%s,%u,%u).' % \
              (','.join(ip.split('.')), port >> 8 & 0xFF, port & 0xFF)
        self.send_byte(msg)

    def start_datasock(self):
        if self.pasv_mode:
            self.datasock, addr = self.servsock.accept()
        else:
            self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.datasock.connect((self.dataAddr, self.dataPort))

    def stop_datasock(self):
        self.datasock.close()
        if self.pasv_mode:
            self.servsock.close()

    def LIST(self, cmd):
        self.send_byte('150 Here comes the directory listing.')
        self.start_datasock()
        self.datasock.send('\r\n'.encode())
        self.stop_datasock()
        self.send_byte('226 Directory send OK.')

    def MKD(self, cmd):
        self.send_byte('257 Directory created.')

    def RMD(self, cmd):
        self.send_byte('250 Directory deleted.')

    def DELE(self, cmd):
        self.send_byte('250 File deleted.')

    def RNFR(self, cmd):
        self.send_byte('350 Ready.')

    def RNTO(self, cmd):
        self.send_byte('250 File renamed.')

    def REST(self, cmd):
        self.send_byte('250 File position reseted.')

    def RETR(self, cmd):
        self.send_byte('150 Opening data connection.')
        self.start_datasock()
        self.datasock.send(' \r\n'.encode())
        self.stop_datasock()
        self.send_byte('226 Transfer complete.')

    def FEAT(self, cmd):
        self.send_byte('211-Extensions supported:')
        self.send_byte(' MLST size*;create;modify*;perm;media-type')
        self.send_byte('211 END')

    def STOR(self, cmd):
        self.send_byte('150 Opening data connection.')
        self.start_datasock()
        while True:
            data = self.datasock.recv(int(self.data_recv_size))
            if not data: break
        self.stop_datasock()
        self.send_byte('226 Transfer complete.')


def start_operation():
    ftp_queue_size = int(conf_th.get_item(q_key='general').get('ftp_queue_size'))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(ftp_queue_size)
        log_th.log_info('{}:{} socket started..'.format(host, str(port)))
    except socket.error as message:
        if s:
            s.close()
            log_th.log_error(message)
        sys.exit(1)

    while 1:
        conn, client_addr = s.accept()
        thread.start_new_thread(FTPServer().ftp_thread, (conn, client_addr))


def server_init(log_set, conf_set, header_set, commands_w_set, data_w_set):
    global log_th, conf_th, header_th, command_w_th, data_w_th, host, port
    log_th = log_set
    conf_th = conf_set
    header_th = header_set
    command_w_th = commands_w_set
    data_w_th = data_w_set
    host = conf_set.get_item(q_key='general').get('sock_ip')
    port = int(conf_set.get_item(q_key='general').get('port'))
