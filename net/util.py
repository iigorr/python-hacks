import socket

def check_connection(hostname, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  ip = socket.gethostbyname(hostname)
  sock.settimeout(1)
  result = sock.connect_ex((ip, 22))
  return (result == 0)