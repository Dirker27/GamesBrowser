import socket

'''t_host = '' 
t_port = 50000 
t_backlog = 5 
t_size = 1024 
t_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
t_s.bind((host,port)) 
t_s.listen(backlog) 
while 1: 
    client, address = s.accept() 
    data = client.recv(size) 
    if data: 
        client.send(data) 
    client.close() 


host = 'localhost'
port = 50000
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
s.send('Hello, world') 
data = s.recv(size) 
s.close() 
print 'Received:', data'''

class echo_server(object):
    def __init__(self):
        self.host = '' 
        self.port = 50000 
        self.backlog = 5 
        self.size = 1024 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def echo(self):
        self.s.bind((self.host, self.port))
        print 'bind'
        self.s.listen(self.backlog)
        print 'listen'
        client, address = self.s.accept()
        print 'accept'
        data = client.recv(self.size) 
        if data: 
            client.send(data) 
        client.close()

class echo_client(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self):
        self.s.connect((self.host, self.port))
        s.send('Hello, World')

    def recieve(self):
        data = s.recv(self.size) 
        s.close() 
        print 'Received:', data


e = echo_server()
print 'echo'
c = echo_client()
print 'client'

for i in range(5):
    e.s.accept()
    c.send()
    e.echo()
    print i
    c.recieve()
