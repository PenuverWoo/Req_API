import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostbyname('192.168.0.7')
# port = 20001
# s.bind((host,port))
s.connect(('10.12.36.185', 20001))

recv_data = s.recv(1024)
recv_data = recv_data.decode("utf-8")

print('recv data:', recv_data)

s.close()