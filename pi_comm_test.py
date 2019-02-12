import socket
import threading
import time

timemacro = lambda: time.strftime('%m-%d GMT %H:%M', time.gmtime())
retry_period = 3

# Connect the socket to the port where the server is listening
# server_address = ('localhost', 8789)
server_address = ('raspberrypi.local', 8789)
print('connecting to {} port {}'.format(*server_address))

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(server_address)
        sock.connect(server_address)
        sock.settimeout(5)
    except (ConnectionRefusedError, socket.gaierror):
        print('Could not connect to pi. Waiting %d sec to try again' % retry_period)
        time.sleep(retry_period)
        continue
    except Exception as e:
        print(e)
        break

    try:
        while True:
            msg = b'1'
            print('sending {!r}'.format(msg))
            sock.sendall(msg)

            data = sock.recv(1)
            print('received {!r}'.format(data))

            time.sleep(1)
    except (ConnectionResetError, IOError):
        print('[{}] Pi went offline.'.format(timemacro()))
        continue
    except Exception as e:
        print('[{}] Something went wrong. stopping.'.format(timemacro()))
        print(e)
        break
    finally:
        sock.close()
