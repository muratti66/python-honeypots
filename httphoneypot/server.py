import socket  # Networking support
import signal  # Signal support (server shutdown on signal receive)
import time    # Current time

# import library
# import tcp_handler



# Created Log Object
#
import library
import tcp_handler

log_ops = library.LogOperation()
# Created Config Object
conf_ops = library.ConfigParse(log_object=log_ops)
# Created Header Writer Object
header_ops = library.HeaderWriter(log_object=log_ops)
# Created Commands Writer Object
commands_w_ops = library.SMTPCommandWriter(log_object=log_ops)
# Created Data Writer Object
data_w_ops = library.DATAWriter(log_object=log_ops)

sock_ip = conf_ops.get_item(q_key='general').get('sock_ip')
port = int(conf_ops.get_item(q_key='general').get('port'))

signal.signal(signal.SIGINT, tcp_handler.graceful_shutdown)

log_ops.log_info('{}:{} socket started..'.format(sock_ip, str(port)))
tcp_handler.server_init(log_set=log_ops, conf_set=conf_ops, data_w_set=data_w_ops,
                        header_set=header_ops, commands_w_set=commands_w_ops)
s = tcp_handler.HTTPServer()
s.activate_server()
