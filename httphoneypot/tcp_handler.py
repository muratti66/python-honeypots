import socket  # Networking support
import time  # Current time

from library import id_generate

host = None
port = None
log_th = None
conf_th = None
header_th = None
command_w_th = None
data_w_th = None

class HTTPServer:

    def __init__(self):
        global host, port, log_th, conf_th, header_th, command_w_th, data_w_th
        self.host = host
        self.port = port
        self.conf_th_ic = conf_th
        self.header_th_ic = header_th
        self.command_w_th_inc = command_w_th
        self.data_w_th_inc = data_w_th
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log_th = log_th
        self.id = None
        self.client_ip = None
        self.client_port = None
        self.hostname = conf_th.get_item(q_key='general').get('hostname')
        self.http_queue_size = int(conf_th.get_item(q_key='general').get('http_queue_size'))
        self.http_recv_size = int(conf_th.get_item(q_key='general').get('http_recv_size'))
        self.server_header_information = conf_th.get_item(q_key='general').get('server_header_information')
        self.html_message = conf_th.get_item(q_key='general').get('html_message')
        self.post_message = conf_th.get_item(q_key='general').get('post_after_message')
        self.sleep_between = int(conf_th.get_item(q_key='general').get('sleep_between'))
        self.no_answer = int(conf_th.get_item(q_key='general').get('no_answer'))

    def activate_server(self):
        try:
            self.socket.bind((self.host, self.port))
        except Exception as e:
            self.log_th.log_error("Warning: Could not aquite port:" + str(self.port) + "\n")
            graceful_shutdown(s=self.socket)

        self._wait_for_connections()

    def shutdown(self):
        try:
            self.log_th.log_info("Shutting down the server")
            self.socket.shutdown()

        except Exception as e:
            self.log_th.log_error("Warning: could not shut down the socket. Maybe it was already closed? : " + e)

    def _gen_headers(self, code):
        h = ''
        if code == 200:
            h = 'HTTP/1.1 200 OK\n'
        elif code == 404:
            h = 'HTTP/1.1 404 Not Found\n'

        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += 'Date: ' + current_date + ' GMT' + '\n'
        h += 'Server: ' + self.server_header_information + '\n'
        # h += 'Connection: close\n\n'
        h += '\n\n'
        return h

    def _wait_for_connections(self):
        while True:
            self.socket.listen(self.http_queue_size)  # maximum number of queued connections
            conn, addr = self.socket.accept()

            self.client_ip = addr.__getitem__(0)
            self.client_port = addr.__getitem__(1)
            self.id = id_generate(size=16)
            self.log_th.log_info('{}:{} connected'.format(self.client_ip, self.client_port))
            header_th.write_header(ip=addr.__getitem__(0), qid=self.id)

            if self.no_answer != 0:
                while True:
                    conn.recv(self.http_recv_size)

            if self.sleep_between != 0:
                time.sleep(self.sleep_between)

            data = conn.recv(self.http_recv_size)
            string = bytes.decode(data)

            request_method = string.split(' ')[0]
            file_requested = string.split(' ')
            file_requested = file_requested[1]

            file_requested = file_requested.split('?')[0]
            if file_requested == '/':
                file_requested = '/index.html'
            url_path = "http://" + self.hostname + ":" + str(self.port) + file_requested
            commands = "Request : " + request_method + ", Access Path : " + url_path
            self.command_w_th_inc.write_commands(data=commands, qid=self.id)
            self.log_th.log_info('{} - {} client request {} - {} '.format(
                self.id, self.client_ip, request_method, url_path))
            self.data_w_th_inc.write_data(data=string, qid=self.id)
            response_headers = self._gen_headers(200)
            if file_requested.split('/')[1] == 'robots.txt':
                response_content = 'User-agent: *' + '\n' + 'Disallow: /' + '\n'
                response_content = response_content.encode()
            elif file_requested.split('/')[1] == 'favicon.ico':
                response_headers = self._gen_headers(404)
                response_content = ''.encode()
            elif request_method == 'POST':
                response_content = self.post_message.encode()
            else:
                response_content = self.html_message.encode()
            server_response = response_headers.encode()
            server_response += response_content

            conn.send(server_response)
            self.log_th.log_info('{}:{} disconnected'.format(self.client_ip, self.client_port))
            conn.shutdown(socket.SHUT_RD)
            conn.close()


def graceful_shutdown(s, sig, dummy):
    s.socket.shutdown()
    import sys
    sys.exit(1)


def server_init(log_set, conf_set, header_set, commands_w_set, data_w_set):
    global log_th, conf_th, header_th, command_w_th, data_w_th, host, port
    log_th = log_set
    conf_th = conf_set
    header_th = header_set
    command_w_th = commands_w_set
    data_w_th = data_w_set
    host = conf_set.get_item(q_key='general').get('sock_ip')
    port = int(conf_set.get_item(q_key='general').get('port'))
