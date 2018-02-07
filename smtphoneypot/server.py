
# Murat B. on github..

import threading
import tcp_handler
import library

# Created Log Object
log_ops = library.LogOperation()
# Created Config Object
conf_ops = library.ConfigParse(log_object=log_ops)
# Created Header Writer Object
header_ops = library.HeaderWriter(log_object=log_ops)
# Created Commands Writer Object
commands_w_ops = library.SMTPCommandWriter(log_object=log_ops)

if __name__ == "__main__":
    """
    Main Method
    """
    # Get Following Variables from Config Files
    server = tcp_handler.server_init(log_set=log_ops, conf_set=conf_ops,
                                     header_set=header_ops, commands_w_set=commands_w_ops)
    sock_ip = conf_ops.get_item(q_key='general').get('sock_ip')
    port = int(conf_ops.get_item(q_key='general').get('port'))
    log_ops.log_info('{}:{} socket started..'.format(sock_ip, str(port)))
    # Opening socket and threads
    try:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        log_ops.log_info('{} thread started..'.format(server_thread.name))
    except Exception as aex:
        log_ops.log_error('Exception!!, {}, program exited...'.format(str(aex)))
        server.server_close()
