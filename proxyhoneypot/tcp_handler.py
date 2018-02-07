import sys, socket
import _thread as thread
import time
from library import id_generate

host = None
port = None
log_th = None
conf_th = None
header_th = None
command_w_th = None
data_w_th = None


class ProxyServer:

    def __init__(self):
        global host, port, log_th, conf_th, header_th, command_w_th, data_w_th
        self.host = host
        self.port = port
        self.conf_th_ic = conf_th
        self.header_th_ic = header_th
        self.command_w_th_inc = command_w_th
        self.data_w_th_inc = data_w_th
        self.log_th = log_th
        self.hostname = conf_th.get_item(q_key='general').get('hostname')
        self.http_queue_size = int(conf_th.get_item(q_key='general').get('http_queue_size'))
        self.http_recv_size = int(conf_th.get_item(q_key='general').get('http_recv_size'))
        self.server_header_information = conf_th.get_item(q_key='general').get('server_header_information')
        self.html_message = conf_th.get_item(q_key='general').get('html_message')
        self.proxy_empty_message = conf_th.get_item(q_key='general').get('proxy_empty_message')
        self.sleep_between = int(conf_th.get_item(q_key='general').get('sleep_between'))
        self.no_answer = int(conf_th.get_item(q_key='general').get('no_answer'))


    def gen_headers(self, code):
        h = ''
        if code == 200:
            h = 'HTTP/1.1 200 OK\n'
        elif code == 404:
            h = 'HTTP/1.1 404 Not Found\n'
        elif code == 403:
            h = 'HTTP/1.1 403 Forbidden\n'
        elif code == 400:
            h = 'HTTP/1.1 400 Bad Request\n'

        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += 'Date: ' + current_date + ' GMT' + '\n'
        h += 'Server: ' + self.server_header_information + '\n'
        h += '\n\n'
        return h

    def client_disconnected(self, conn):
        conn.close()

    def proxy_thread(self, conn, client_addr):
        id = id_generate(size=16)
        client_ip = client_addr[0]
        client_port = str(client_addr[1])
        self.log_th.log_info('{}:{} connected to proxy socket'.format(client_ip, client_port))
        commands = "Client : " + client_ip + ":" + client_port + " is connected to proxy://" \
                   + self.hostname + ":" + str(self.port)
        self.command_w_th_inc.write_commands(data=commands, qid=id)
        if self.no_answer != 0:
            while True:
                conn.recv(self.http_recv_size)

        if self.sleep_between != 0:
            time.sleep(self.sleep_between)

        header_th.write_header(ip=client_addr.__getitem__(0), qid=id)
        request = conn.recv(self.http_recv_size)
        first_line = bytes.decode(request).split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        destination = webserver + ":" + str(port)
        commands = "Client : " + client_ip + ":" + client_port + ", Trying access to : " + destination
        self.command_w_th_inc.write_commands(data=commands, qid=id)
        self.log_th.log_info('{} - {}:{} client trying access to {} '.format(
            id, client_ip, client_port, destination))

        self.data_w_th_inc.write_data(data=bytes.decode(request), qid=id)
        header = self.gen_headers(403)
        response = self.html_message
        try:
            if port != 80:
                header = self.gen_headers(400)
                response = ' '
                self.log_th.log_info('{} - {}:{} access denied, destination port is : {} '.format(
                    id, client_ip, client_port, str(port)))
                conn.shutdown(socket.SHUT_RD)
                conn.close()
            if webserver.strip() == "":
                response = self.proxy_empty_message
            final_response = header + response
            conn.send(bytes(final_response.encode()))
        except Exception as e:
            import traceback
            try:
                raise TypeError("Again !?!")
            except:
                pass
        conn.shutdown(socket.SHUT_RD)
        conn.close()


def start_operation():
    http_queue_size = int(conf_th.get_item(q_key='general').get('http_queue_size'))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
        s.listen(http_queue_size)
        log_th.log_info('{}:{} socket started..'.format(host, str(port)))
    except socket.error as message:
        if s:
            s.close()
            log_th.log_error("Could not open socket:", message)
        sys.exit(1)

    while 1:
        conn, client_addr = s.accept()
        thread.start_new_thread(ProxyServer().proxy_thread, (conn, client_addr))


def server_init(log_set, conf_set, data_w_set, header_set, commands_w_set):
    global log_th, conf_th, header_th, command_w_th, data_w_th, host, port
    log_th = log_set
    conf_th = conf_set
    header_th = header_set
    command_w_th = commands_w_set
    data_w_th = data_w_set
    host = conf_set.get_item(q_key='general').get('sock_ip')
    port = int(conf_set.get_item(q_key='general').get('port'))
