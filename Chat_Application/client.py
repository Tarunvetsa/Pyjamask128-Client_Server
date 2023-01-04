import socket
host = socket.gethostname() #getting host
port = 4515
#creating the socket and connecting to host,port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port)) 
print("Connecting to the server \n")
print("\n----------Chat Begins----------\n")
print("\nTo exit chat enter 'bye'\n")

x=input("You:")
while x.lower()!="bye":
  s.send(bytes(x,'utf-8'))
  msg=s.recv(1024).decode()
  print("->",msg)
  x=input("You:")
s.send(bytes(x,'utf-8'))
print("->",s.recv(1024).decode())

s.close()
