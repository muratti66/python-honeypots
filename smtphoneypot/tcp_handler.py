# Murat B. on github..

import threading
import library as library
import socketserver
import time

log_th = None
conf_th = None
header_th = None
command_w_th = None


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    # Creating default variables
    hostname = str()
    message_id = str()
    client_ip = str()
    client_port = int()
    sdt_recv_size = int()
    data_recv_size = int()
    mail_save_enable = int()
    mail_save_path = str()
    no_answer = int()
    sleep_between = int()
    conf_th_ic = None

    def func_sender(self, message):
        self.request.sendall('{}\r\n'.format(message).encode())
        self.command_w_th_inc.write_commands(data=message, qid=self.message_id)

    def setup(self):
        """
        Settings default variables and sending first message
        :return: None
        """
        global log_th, conf_th, header_th, command_w_th
        self.conf_th_ic = conf_th
        self.header_th_ic = header_th
        self.command_w_th_inc = command_w_th
        self.hostname = conf_th.get_item(q_key='general').get('hostname')
        self.std_recv_size = int(conf_th.get_item(q_key='general').get('std_recv_size'))
        self.data_recv_size = int(conf_th.get_item(q_key='general').get('data_recv_size'))
        self.mail_save_enable = int(conf_th.get_item(q_key='general').get('mail_save_enable'))
        self.mail_save_path = conf_th.get_item(q_key='general').get('mail_save_path')
        self.no_answer = int(conf_th.get_item(q_key='general').get('no_answer'))
        self.sleep_between = int(conf_th.get_item(q_key='general').get('sleep_between'))
        self.message_id = library.q_id_generate(size=16)
        self.client_ip = tuple(self.client_address).__getitem__(0)
        self.client_port = int(tuple(self.client_address).__getitem__(1))
        # Running
        self.header_th_ic.write_header(ip=self.client_ip, qid=self.message_id)
        message = '220 ' + self.hostname
        self.func_sender(message)
        log_th.log_info('{} connected to {} thread'.format(self.client_ip, threading.current_thread().name))

    def finish(self):
        """
        Thread stopping, if client exit
        :return: None
        """
        global log_th
        log_th.log_info('{} disconnected from {} thread'.format(self.client_ip, threading.current_thread().name))

    def func_denied(self, message):
        """
        Denied mesage log and sending
        :param message: message
        :return: None
        """
        log_th.log_info('{} - {} wrong entry : "{}"'.format(self.message_id, self.client_ip, message))
        self.func_sender(message)

    def func_ehlo(self, data):
        """
        Ehlo message send, if need a ehlo
        :param data: Received Byte Code
        :return: Boolean
        """
        data_list = bytes(data).decode().encode('ascii', 'ignore').decode().split(' ')
        if data_list[0].lower().rstrip() == 'ehlo':
            message = '250-' + self.hostname + '\r\n250-PIPELINING\r\n' \
                      + '250-8BITMIME\r\n250-SIZE ' \
                      + str(self.data_recv_size) \
                      + '\r\n' + '250 AUTH LOGIN PLAIN'
            self.func_sender(message)
            return True

    def func_helo(self, data):
        """
        Helo message send, if need a helo
        :param data: Received Byte Code
        :return: Boolean
        """
        data_list = bytes(data).decode().encode('ascii', 'ignore').decode().split(' ')
        if data_list[0].lower().rstrip() == 'helo':
            message = '250 {}'.format(self.hostname)
            self.func_sender(message)
            return True

    def func_rset(self, data):
        """
        Rset message send, if need a rset
        :param data: Received Byte Code
        :return: Boolean
        """
        if bytes(data).decode().encode('ascii', 'ignore').decode().lower().rstrip() == 'rset':
            message = '250 OK'
            self.func_sender(message)
            return True

    def func_empty_check(self, data):
        """
        Empty message check function
        :param data: Received Byte Code
        :return: Boolean
        """
        check = bytes(data).decode().encode('ascii', 'ignore').decode().lower().rstrip()
        if str(check) == '':
            self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('command not found'))
            return True

    def func_starttls(self, data):
        """
        Starttls message send, if need a starttls
        :param data: Received Byte Code
        :return: Boolean
        """
        check = bytes(data).decode().encode('ascii', 'ignore').decode().lower().rstrip()
        if check == 'starttls':
            self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get(check))
            return True

    def func_auth(self, data):
        """
        Auth Login message send, if need a auth
        :param data: Received Byte Code
        :return: Boolean
        """
        check = bytes(data).decode().encode('ascii', 'ignore').decode().lower().rstrip()
        if check == 'auth login':
            auth_id = library.q_id_generate(size=12)
            message = '334 ' + auth_id
            self.func_sender(message)
            self.request.recv(self.std_recv_size)
            auth_id_two = library.q_id_generate(size=12)
            message_two = '334 ' + auth_id_two
            self.func_sender(message_two)
            self.request.recv(self.std_recv_size)
            message_three = self.conf_th_ic.get_item(q_key='std-messages').get(check)
            self.func_sender(message_three)
            return True

    def func_auth_plain(self, data):
        check = bytes(data).decode().encode('ascii', 'ignore').decode().lower().rstrip()
        if check == 'auth plain':
            check = check.split(' ')
            if check.__len__() == 2:
                message = '334'
                self.func_sender(message)
                self.request.recv(self.std_recv_size)
                message_two = self.conf_th_ic.get_item(q_key='std-messages').get('auth login')
                self.func_sender(message_two)
                return True
            elif check.__len__() == 3:
                message = self.conf_th_ic.get_item(q_key='std-messages').get('auth login')
                self.func_sender(message)
                return True

    def func_from(self, data, get_recv):
        """
        Mail from message send, if need a from
        :param data: Received Byte Code
        :param get_recv: Boolean
        :return: Boolean
        """
        if get_recv:
            checking = bytes(data).decode().encode('ascii', 'ignore').decode()
        else:
            checking = bytes(data).decode().encode('ascii', 'ignore').decode().splitlines()[0]
        data_list = checking.split(':')
        remove_bracket = str(data_list[1])
        remove_bracket = remove_bracket[2:-1]
        data_list[1] = remove_bracket
        check = data_list[0].lower().rstrip()
        if check == 'mail from':
            message = self.conf_th_ic.get_item(q_key='std-messages').get(check)
            self.func_sender(message)
            return True

    def func_to(self, data, get_recv, get_data):
        """
        Rcpt to message send, if need a to
        :param data: Received Byte Code
        :param get_recv: Boolean
        :param get_data: Boolean
        :return: Boolean
        """
        checking = bytes(data).decode().encode('ascii', 'ignore').decode()
        if not get_data:
            checking = bytes(data).decode().encode('ascii', 'ignore').decode().splitlines()[0]
        if not get_recv:
            checking = bytes(data).decode().encode('ascii', 'ignore').decode().splitlines()[1]
        try:
            data_list = checking.split(':')
            remove_bracket = str(data_list[1])
            remove_bracket = remove_bracket[2:-1]
            data_list[1] = remove_bracket
            check = data_list[0].lower().rstrip()
            if check == 'rcpt to':
                message = self.conf_th_ic.get_item(q_key='std-messages').get(check)
                self.func_sender(message)
                return True
        except:
            return False

    def func_data(self, data, get_recv, get_data):
        """
        Data message send, if need a Data
        :param data: Received Byte Code
        :param get_recv: Boolean
        :param get_data: Boolean
        :return: Boolean
        """
        if get_data:
            checking = bytes(data).decode().encode('ascii', 'ignore').decode().lower().rstrip()
        else:
            checking = bytes(data).decode().encode('ascii', 'ignore').decode().splitlines()[1].lower().rstrip()
        if checking == 'data':
            message = self.conf_th_ic.get_item(q_key='std-messages').get(checking)
            self.func_sender(message)
            return True

    def func_data_ok(self):
        """
        Send ok message and queue id
        :return: None
        """
        message = self.conf_th_ic.get_item(q_key='std-messages').get('data ok') + ' {}'.format(self.message_id)
        self.func_sender(message)

    def func_quit(self, data):
        """
        Quit message, if need a quit
        :param data: Received Byte Code
        :return: Boolean
        """
        check = bytes(data).decode().encode('ascii', 'ignore').decode().lower().rstrip()
        if check == 'quit':
            message = self.conf_th_ic.get_item(q_key='std-messages').get(check)
            self.func_sender(message)
            self.finish()
            return True

    def handle(self):
        """
        This method is for all smtp transaction
        :return: None
        """
        global log_th
        sent = 1
        msg_body = ''
        get_recv = True
        get_data = True
        empty_check = 0
        # Looping session requests
        while 1:
            try:
                # If enabled sleep feauture
                if self.sleep_between != 0:
                    time.sleep(self.sleep_between)
                # If no answer feauture
                if self.no_answer != 0:
                    time.sleep(1)
                    continue
                # Changing receive size if receiving data part
                if sent == 3 or sent == 4:
                    data = self.request.recv(self.data_recv_size)
                else:
                    data = self.request.recv(self.std_recv_size)
                if sent != 5:
                    self.command_w_th_inc.write_commands(
                        data=bytes(data).decode().encode('ascii', 'ignore')
                            .decode().rstrip(), qid=self.message_id)
                # To many empty line received, closed thread
                if self.func_empty_check(data):
                    if empty_check >= 3:
                        break
                    else:
                        empty_check += 1
                        continue
                # Logging session requests if steps not equal to data section
                if sent != 5:
                    log_th.log_info('{} - {} client executed : "{}"'.format(
                        self.message_id, self.client_ip, bytes(data).decode().rstrip()))
                # Break the loop
                if self.func_quit(data):
                    break
            except Exception as ae:
                log_th.log_warning('{} encounter an error from {} thread : {}'.format(
                    self.client_ip, threading.current_thread().name, str(ae)))
                break
            else:
                try:
                    # Checking the all steps
                    if self.func_rset(data):
                        sent = 2
                        continue
                    if self.func_auth(data):
                        continue
                    if self.func_auth_plain(data):
                        continue
                    if self.func_starttls(data):
                        continue
                    # Starting the sent steps
                    # Ehlo/hello
                    if sent == 1:
                        if self.func_ehlo(data) or self.func_helo(data):
                            sent += 1
                        else:
                            self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('command not found'))
                    # Mail from, rcpt to, data
                    elif sent == 2:
                        if bytes(data).decode().encode('ascii', 'ignore').decode().rstrip().splitlines().__len__() > 2:
                            get_data = False
                            get_recv = False
                        elif bytes(data).decode().encode('ascii',
                                                         'ignore').decode().rstrip().splitlines().__len__() > 1:
                            get_recv = False
                        if self.func_from(data, get_recv):
                            sent += 1
                        else:
                            self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('mail from'))
                        if not get_recv:
                            if self.func_to(data, get_recv, get_data):
                                sent += 1
                                get_recv = True
                            else:
                                self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('rcpt to'))
                        if not get_data:
                            if self.func_data(data, get_recv, get_data):
                                sent += 1
                                get_data = True
                            else:
                                self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('data'))
                    # rcpt to and data
                    elif sent == 3:
                        if bytes(data).decode().encode('ascii', 'ignore').decode().rstrip().splitlines().__len__() > 1:
                            get_data = False
                        if self.func_to(data, get_recv, get_data):
                            sent += 1
                        else:
                            self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('rcpt to'))
                        if not get_data:
                            if self.func_data(data, get_recv, get_data):
                                sent += 1
                                get_data = True
                            else:
                                self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('data'))
                    # data
                    elif sent == 4:
                        if self.func_to(data, get_recv, get_data):
                            continue
                        if self.func_data(data, get_recv, get_data):
                            sent += 1
                        else:
                            self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('data'))
                    # content writing to file (if enabled) and quit statement
                    elif sent == 5:
                        data_list = bytes(data).decode().split('\r\n')
                        for line in data_list:
                            if str(line) == '.':
                                if self.mail_save_enable != 0:
                                    out_file = open(self.mail_save_path + '/'
                                                    + self.message_id + '.eml', 'w')
                                    out_file.write(msg_body)
                                    out_file.close()
                                self.func_data_ok()
                                sent = 1
                                break
                            else:
                                msg_body += str(line) + '\r\n'
                except IndexError:
                    if sent == 2:
                        self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('mail from'))
                    elif sent == 3:
                        self.func_denied(self.conf_th_ic.get_item(q_key='err-messages').get('rcpt to'))


def server_init(log_set, conf_set, header_set, commands_w_set):
    """
    First initializor for tcp handler
    :param log_set: Log Object
    :param conf_set: Config Object
    :return: Threaded Tcp Server Object
    """
    global log_th, conf_th, header_th, command_w_th
    log_th = log_set
    conf_th = conf_set
    header_th = header_set
    command_w_th = commands_w_set
    sock_ip = conf_set.get_item(q_key='general').get('sock_ip')
    port = int(conf_set.get_item(q_key='general').get('port'))
    return ThreadedTCPServer((sock_ip, port), ThreadedTCPRequestHandler)
