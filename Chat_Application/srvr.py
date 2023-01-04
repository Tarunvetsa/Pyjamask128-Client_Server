import socket
port = 4515
host =socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port)) #creating and binding the socket
s.listen(2) #wiating for the client
print("(->) means received from client")
print("(<-) means sending to client\n")   
print('\nListening for the clients to connect \n')
while True:
    c, address = s.accept() #accepting the client connection
   
    if c:
        print('connecting to',address)
    
    msg=c.recv(1024).decode()
    print("-> ",msg)
    while msg!="bye":
        print("<-",end=" ")
        servr_msg=input()
        c.send(bytes(servr_msg,'utf-8'))
        msg=c.recv(1024).decode()
        print("-> ",msg)
    print("<- Ok Bye")
    c.send(bytes("Ok Bye",'utf-8'))
    print('\nDisconnected with',address)
    c.close()