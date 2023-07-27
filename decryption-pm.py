import copy

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

def keyscheduling():
    key=input("Enter the Secret key in hex(32 values only):")
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
    
def decr_pm():
    cipher=input("\nEnter the cipher text:")
    cipher_text=[[0 for i in range(32)]for j in range(4)]
    ind=0
    
    for i in range(4):
        for j in range(32):
            cipher_text[i][j]=int(cipher[ind])
            ind+=1
    Sbox = ['0010', '1101', '0011', '1001', '0111', '1011', '1010', '0110', '1110', '0000', '1111', '0100', '1000', '0101', '0001',
    '1100']
    key_lis=keyscheduling()
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
                
    print(text)

plain_text=decr_pm()
