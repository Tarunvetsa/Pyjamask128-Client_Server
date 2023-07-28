# Pyjamask128-Client_Server
Encryption of plain text, decryption of cypher text using Client-Server Application

The working of Pyjamask-128 encryption and decryption process are detailly mentioned in the pdf

The server.py code contains the encryption and decryption code of Pyjamask-128

Open 2 terminals in current repository.

Run the command python3 server.py in 1st terminal, which will listen for clients in specified port mentioned in the code.

Run the command python3 client.py in 2nd terminal,then ---> Enter 1 for encryption process. Then, enter the plain text that you want to encrypt it. Next, enter the key(16 hex values) to encrypt it. (hex values-123456789abcdef) Then server will respond by sending the encrypted text to client.

---> Enter 2 for decryption process. Then, enter the cipher text in binary form 128 bits that you want to decrypt it. Next, enter the key(16 hex values) by using which will decrypt. Then server will respond by sending the decrypted text to client.
