import socket

def start_listener(pi_address, forward_address):
    pi_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pi_sock.connect(pi_address)

    f_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f_sock.bind(forward_address)

    cur_status = 2


start_listener(('169.254.72.29', 8789), ('127.0.0.1', 8787))