# Pyjamask128-Client_Server
Encryption of plain text, decryption of cypher text using Client-Server Application

* Pyjamask128 Client-Server Implementation was based on Pyjamask128 Encryption, decryption methods and the Client-Server Chat Application given in Chat_Application Folder.
* The working of Pyjamask-128 encryption and decryption process are detailly mentioned in the pdf which is present in folder Pyjmask-128_Encryption&Decryption.

* The server.py code contains the encryption and decryption codes of Pyjamask-128 cipher

Redirect to the directory Pyjmask-128_Encryption&Decryption.
```
cd Pyjmask-128_Encryption&Decryption
```

Open 2 terminals in current repository.<br>

Run the command `python3 server.py` in 1st terminal, which will listen for clients in specified port mentioned in the code.<br>

Run the command `python3 client.py` in 2nd terminal,then <br>

---> ``Enter 1 for encryption process.``<br>
&nbsp;&nbsp;&nbsp;&nbsp;Then, enter the plain text that you want to encrypt it.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Next, enter the key(16 hex values) to encrypt it.     (hex values-123456789abcdef) <br>
&nbsp;&nbsp;&nbsp;&nbsp;Then server will respond by sending the encrypted text to client. <br>

---> ``Enter 2 for decryption process.``<br>
&nbsp;&nbsp;&nbsp;&nbsp;Then, enter the cipher text in binary form 128 bits that you want to decrypt it.<br> 
&nbsp;&nbsp;&nbsp;&nbsp;Next, enter the key(16 hex values) by using which will decrypt.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Then server will respond by sending the decrypted text to client.<br>
