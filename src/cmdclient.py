from socket import *

host = "127.0.0.1"
port = 21567
buf = 1024
addr = (host, port)
udp_sock = socket(AF_INET, SOCK_DGRAM)
udp_sock.sendto('col_hard' , addr)
udp_sock.close()
print "ENVIADO"