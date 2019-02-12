import socket
import wiringpi

sensor_pin = 16

if __name__ == '__main__':
  wiringpi.wiringPiSetup()
  wiringpi.pinMode(sensor_pin, 0)

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(('raspberrypi.local', 8789))
  sock.listen(1)

  while True:
    client_sock, client_address = sock.accept()
    client_sock.settimeout(5)
    print('Connection from', client_address)
    try:
      while True:
        data = client_sock.recv(1)
        if data:
          door_state = not wiringpi.digitalRead(sensor_pin)
          # print('got {!r}, sending {}'.format(data, door_state))
          if door_state:
            client_sock.sendall(b'1')
          else:
            client_sock.sendall(b'0')
        else:
          break
    except socket.timeout:
      continue
    finally:
      print('Closing connection')
      client_sock.close()
