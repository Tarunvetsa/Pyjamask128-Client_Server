import socket,copy
port = 6518
host =socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port)) #creating and binding the socket
s.listen(2) #wiating for the client
# print("(->) means received from client")
# print("(<-) means sending to client\n")   
print('\nListening for the clients to connect \n')
while True:
    c, address = s.accept() #accepting the client connection
    option=c.recv(1024).decode()

    if c:
        print('connecting to',address)
    if option=="1":
        plaintext=c.recv(1024).decode()
        key_rnds=c.recv(1024).decode()
    
        
        def col_diff(keybef):
            m=[[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
            for i in range(32):
                xor=0
                for j in range(4):
                    for k in range(4):
                        xor=(xor)^(m[j][k]^keybef[k][i])

                    keybef[j][i]=xor
            return keybef

        def row1(A,B):

            result = [[0] for i in range(32)]
            s=[]
            for i in range(len(B)):
                s.append([B[i]])
        #     print(s)
        #     print(A)
            for i in range(len(A)):
                for j in range(len(s[0])):
                    for k in range(len(s)):
                        u=copy.deepcopy(result[i][j])
        #                 print((A[i][k] ^ s[k][j]),u ^ (A[i][k] ^ s[k][j]))
                        result[i][j] = (u ^ (A[i][k] * s[k][j]))

        #         print(result[i][j])

            final=[]
        #     print(result)
            for i in range(32):
                final.append(result[i][0])

            return final

        def circulant( arr,  n):
        
            c = [[0 for i in range(n)] for j in range(n)]
            for k in range(n):
                c[k][0] = arr[k]

            for  i in range(1,n):
                for j in range(n):
                    if (j - 1 >= 0):
                        c[j][i] = c[j - 1][i - 1]
                    else:
                        c[j][i] = c[n - 1][i - 1]


            result = [[c[j][i] for j in range(len(c))] for i in range(len(c[0]))]

            return result

        def row_diff(key_state):

            l=[1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0]
            mk=circulant(l,32)
            key_state[0]=row1(mk,key_state[0])
            key_state[1]=key_state[1][8:]+key_state[1][0:8]
            key_state[2]=key_state[2][15:]+key_state[2][0:15]
            key_state[3]=key_state[3][18:]+key_state[3][0:18]

            return key_state

        def con_add(key_state,x):
            con = [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]
            for i in range(8):
                key_state[3][i]^=con[i]
            for i in range(8,16):
                key_state[2][i]^=con[i]
            for i in range(16,24):
                key_state[1][i]^=con[i]
            for i in range(24,28):
                key_state[0][i]^=con[i]
            u=bin(x)[2::].zfill(4)
            for i in range(4):
                key_state[0][28+i]^=int(u[i])
            return key_state

        def keyscheduling(key):

            key_bin=bin(int(key,16))[2::].zfill(128)
            key_state=[[0 for i in range(32)]for j in range(4)]
            # print(key_bin,'\n',key_state,len(key_bin))

            x=0
            for i in range(4):
                for j in range(32):
                    key_state[i][j]=int(key_bin[x])
                    x+=1
            # print(key_state)

            key_list=[key_state]
            for rnd in range(14):            
                key_state=col_diff(key_state)
                key_state=row_diff(key_state)
                key_state=con_add(key_state,rnd)
            #     print(key_state)
                k = copy.deepcopy(key_state)
                key_list.append(k)


            return key_list
        keys=keyscheduling(key_rnds)
        # print(keyscheduling())

        M0 = [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0]
        M1 = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1]
        M2 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1]
        M3 = [0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1]
        mk0=circulant(M0,32)
        mk1=circulant(M1,32)
        mk2=circulant(M2,32)
        mk3=circulant(M3,32)

        def addrndkey(k,state):
            result=[[0 for i in range(32)]for j in range(4)]
            for i in range(4):
                for j in range(32):
                    result[i][j] = k[i][j] ^ state[i][j]
            return result


        def subbytes(sbox,state):
            for i in range(32):
                x=""
                for j in range(4):
                    x+=str(state[j][i])
        #         print(int(x,2))
                y=sbox[int(x,2)]

                for k in range(4):
                    state[k][i]=int(y[k])
            return state

        def mixrows(A,B):

            result = [[0] for i in range(32)]

            s=[]
            for i in B:
                s.append([B[i]])
        #     print(s)
            for i in range(len(A)):
        #         print(A[i])
                for j in range(len(s[0])):
                    for k in range(len(s)):
                        u=copy.deepcopy(result[i][j])
                        result[i][j] = u^(A[i][k]^s[k][j])

            final=[]
        #     print(result)
            for i in range(32):
                final.append(result[i][0])

            return final

        def encr_pm(message):    
            Sbox = ['0010', '1101', '0011', '1001', '0111', '1011', '1010', '0110', '1110', '0000', '1111', '0100', '1000', '0101', '0001',
            '1100']
            in_bin=""
            for i in message:
                x=ord(i)
            #     print(format(x, '#010b'))
                in_bin+=str(format(x, '#010b')[2:])
            # print(len(in_bin))
            if len(in_bin)<128:
                in_bin=in_bin.zfill(128)

            
            input_state=[[0 for i in range(32)]for j in range(4)]
            # # print(key_bin,'\n',key_state,len(key_bin))

            x=0
            for i in range(4):
                for j in range(32):
                    input_state[i][j]=int(in_bin[x])
                    x+=1

            # print(input_state)
            print()

            for i in range(14):
                input_state=addrndkey(keys[i],input_state)
            #     print(input_state)

            #     print()
                input_state=subbytes(Sbox,input_state)
            #     print(input_state)
            #     print()
                input_state[0]=mixrows(mk0,input_state[0])
            #     print(input_state[0])
                input_state[1]=mixrows(mk1,input_state[1])
            #     print(input_state[1])
                input_state[2]=mixrows(mk2,input_state[2])
            #     print(input_state[2])
                input_state[3]=mixrows(mk3,input_state[3])
            #     print(input_state[3])
            #     print()
            input_state=addrndkey(keys[14],input_state)
            r=""
            for i in range(4):
                for j in range(32):
                    r+=str(input_state[i][j])
            return r


        cipher_text=encr_pm(plaintext)
       
        c.send(bytes(cipher_text,'utf-8'))
        
        c.close()

    if option=="2":
        inp=c.recv(1024).decode()
        key_rnds=c.recv(1024).decode()
    
        if c:
            print('connecting to',address)

        def col_diff(keybef):
            m=[[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
            for i in range(32):
                xor=0
                for j in range(4):
                    for k in range(4):
                        xor=(xor)^(m[j][k]^keybef[k][i])

                    keybef[j][i]=xor
            return keybef

        def row1(A,B):
            
            result = [[0] for i in range(32)]
            s=[]
            for i in range(len(B)):
                s.append([B[i]])
        #     print(s)
        #     print(A)
            for i in range(len(A)):
                for j in range(len(s[0])):
                    for k in range(len(s)):
                        u=copy.deepcopy(result[i][j])
        #                 print((A[i][k] ^ s[k][j]),u ^ (A[i][k] ^ s[k][j]))
                        result[i][j] = (u ^ (A[i][k] * s[k][j]))
                        
        #         print(result[i][j])

            final=[]
        #     print(result)
            for i in range(32):
                final.append(result[i][0])
            
            return final
            
        def circulant( arr,  n):
        
            c = [[0 for i in range(n)] for j in range(n)]
            for k in range(n):
                c[k][0] = arr[k]

            for  i in range(1,n):
                for j in range(n):
                    if (j - 1 >= 0):
                        c[j][i] = c[j - 1][i - 1]
                    else:
                        c[j][i] = c[n - 1][i - 1]


            result = [[c[j][i] for j in range(len(c))] for i in range(len(c[0]))]

            return result
            
        def row_diff(key_state):
            
            l=[1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0]
            mk=circulant(l,32)
            key_state[0]=row1(mk,key_state[0])
            key_state[1]=key_state[1][8:]+key_state[1][0:8]
            key_state[2]=key_state[2][15:]+key_state[2][0:15]
            key_state[3]=key_state[3][18:]+key_state[3][0:18]
            
            return key_state

        def con_add(key_state,x):
            con = [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]
            for i in range(8):
                key_state[3][i]^=con[i]
            for i in range(8,16):
                key_state[2][i]^=con[i]
            for i in range(16,24):
                key_state[1][i]^=con[i]
            for i in range(24,28):
                key_state[0][i]^=con[i]
            u=bin(x)[2::].zfill(4)
            for i in range(4):
                key_state[0][28+i]^=int(u[i])
            return key_state

        def keyscheduling(key):

            key_bin=bin(int(key,16))[2::].zfill(128)
            key_state=[[0 for i in range(32)]for j in range(4)]
            # print(key_bin,'\n',key_state,len(key_bin))

            x=0
            for i in range(4):
                for j in range(32):
                    key_state[i][j]=int(key_bin[x])
                    x+=1
            # print(key_state)

            key_list=[key_state]
            for rnd in range(14):            
                key_state=col_diff(key_state)
                key_state=row_diff(key_state)
                key_state=con_add(key_state,rnd)
            #     print(key_state)
                k = copy.deepcopy(key_state)
                key_list.append(k)

            
            return key_list
        key_lis=keyscheduling(key_rnds)
        # print(keyscheduling())

        M01 = [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        M11 = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
        M21 = [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        M31 = [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0]
        mk01=circulant(M01,32)
        mk11=circulant(M11,32)
        mk21=circulant(M21,32)
        mk31=circulant(M31,32)

        def addrndkey(k,state):
            result=[[0 for i in range(32)]for j in range(4)]
            for i in range(4):
                for j in range(32):
                    result[i][j] = k[i][j] ^ state[i][j]
            return result
            
        def invmixrows(A,B):
            result = [[0] for i in range(32)]
            
            s=[]
            for i in B:
                s.append([B[i]])
        #     print(s)
            for i in range(len(A)):
        #         print(A[i])
                for j in range(len(s[0])):
                    for k in range(len(s)):
                        u=copy.deepcopy(result[i][j])
                        result[i][j] = u^(A[i][k]^s[k][j])

            final=[]
        #     print(result)
            for i in range(32):
                final.append(result[i][0])
            
            return final
            
        def invsbox(sbox,state):
            for i in range(32):
                x=""
                for j in range(4):
                    x+=str(state[j][i])
        #         print(int(x,2))
                z=sbox.index(x)
                y=str(bin(z)[2:])
        #         print(y)
                for k in range(0):
                    state[k][i]=int(y[k])
            return state
            
        def decr_pm(cipher):
            cipher_text=[[0 for i in range(32)]for j in range(4)]
            ind=0
            
            for i in range(4):
                for j in range(32):
                    cipher_text[i][j]=int(cipher[ind])
                    ind+=1
            Sbox = ['0010', '1101', '0011', '1001', '0111', '1011', '1010', '0110', '1110', '0000', '1111', '0100', '1000', '0101', '0001',
            '1100']
            cipher_text=addrndkey(key_lis[14],cipher_text)
            for i in range(13,-1,-1):
                cipher_text[0]=invmixrows(mk01,cipher_text[0])
                cipher_text[1]=invmixrows(mk11,cipher_text[1])
                cipher_text[2]=invmixrows(mk21,cipher_text[2])
                cipher_text[3]=invmixrows(mk31,cipher_text[3])
                
                cipher_text=invsbox(Sbox,cipher_text)
                
                cipher_text=addrndkey(key_lis[i],cipher_text)

            bin_str=""
            text=""
            x=0
            # print(cipher_text)
            for i in range(4):
                for j in range(32):
                    bin_str+=str(cipher_text[i][j])
                    x+=1
                    if x==8:
                        # print(int(bin_str,2))
                        text+=chr(int(bin_str,2))
                        bin_str=""
                        x=0
                        
            return text

        plain_text=decr_pm(inp)
        c.send(bytes(plain_text,'utf-8'))
        c.close()