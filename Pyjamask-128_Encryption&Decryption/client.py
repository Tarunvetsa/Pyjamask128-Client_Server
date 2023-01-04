import socket
host = socket.gethostname() #getting host
port = 6518
print("Enter number: \n1 for Pyjamask-128 encryption\n2 for Pyjamask-128 decryption\n")
x=input()
#creating the socket and connecting to host,port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("\nConnecting to the server \n")
s.send(bytes(x,'utf-8'))
if x=="1":
  
  print("Connected with Pyjamask-128 Encryption Server\n")
  print("Enter the message to be encrypted:\n")
  inp_msg=input()
  s.send(bytes(inp_msg,'utf-8'))
  print("\nEnter the secret key(32 hex values only):")
  secret_key=input()
  s.send(bytes(secret_key,'utf-8'))
  cipher_text=s.recv(1024).decode()
  print(cipher_text,"\n")
  s.close()

if x=="2":
  print("Connected with Pyjamask-128 Decryption Server\n")
  print("Enter the ciphertext to be decrypted:\n")
  cip_msg=input()
  s.send(bytes(cip_msg,'utf-8'))
  print("\nEnter the secret key(32 hex values only):")
  secret_key=input()
  s.send(bytes(secret_key,'utf-8'))
  plain_text=s.recv(1024).decode()
  print(plain_text)
  s.close()
