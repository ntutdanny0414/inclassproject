# S-Box
sBox  = [0x9, 0x4, 0xa, 0xb, 0xd, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3, 0xc, 0xe, 0xf, 0x7]
# Inverse S-Box
sBoxI = [0xa, 0x5, 0x9, 0xb, 0x1, 0x7, 0x8, 0xf,
         0x6, 0x0, 0x2, 0x3, 0xc, 0x4, 0xd, 0xe]
def mult(p1, p2):
    p = 0
    while p2:
        if p2 & 0b1:
            p ^= p1
        p1 <<= 1
        if p1 & 0b10000:
            p1 ^= 0b11
        p2 >>= 1
    return p & 0b1111 
def bitmat(m):
    return [m >> 12, (m >> 4) & 0xf, (m >> 8) & 0xf,  m & 0xf]    #4567第3         
def matbit(m):
    return (m[0] << 12) + (m[2] << 8) + (m[1] << 4) + m[3] 
def addKey(s1, s2):
    return [i ^ j for i, j in zip(s1, s2)]
def subNib4(sbox, s):
    return [sbox[e] for e in s]     
def shiftRow(s):
    return [s[0], s[1], s[3], s[2]]
def subNib(b):
    return sBox[b >> 4] + (sBox[b & 0x0f] << 4)#前4個往後後4個往前
def keyExp(key):
    w = [None] * 6
    Rcon1, Rcon2 = 0b10000000, 0b00110000
    w[0] = int(key[:8],2)
    w[1] = int(key[8:],2)
    w[2] = w[0] ^ Rcon1 ^ subNib(w[1])
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ Rcon2 ^ subNib(w[3])
    w[5] = w[4] ^ w[3]
    return w
def mixColumn(s):
    return [s[0] ^ mult(4, s[2]), s[1] ^ mult(4, s[3]),
            s[2] ^ mult(4, s[0]), s[3] ^ mult(4, s[1])]    
def encrypt(plaintext):
    state = bitmat(((w[0] << 8) + w[1]) ^ plaintext)
#    print(state)
    state = subNib4(sBox, state)
#    print(state)
    state = shiftRow(state)
#    print(state)
    state = mixColumn(state)
#    print(state)
    state = addKey(bitmat((w[2] << 8) + w[3]), state)
#    print(state)
    state = subNib4(sBox, state)
#    print(state)
    state = shiftRow(state)
#    print(state)
    state = addKey(bitmat((w[4] << 8) + w[5]), state)
#    print(state)
#    print(matbit(state))
    return matbit(state)
def MixColumni(s):
    return [mult(9, s[0]) ^ mult(2, s[2]), mult(9, s[1]) ^ mult(2, s[3]),
            mult(9, s[2]) ^ mult(2, s[0]), mult(9, s[3]) ^ mult(2, s[1])]     
def decrypt(ciphertext):  
    state = bitmat(((w[4] << 8) + w[5]) ^ ciphertext)
    state = shiftRow(state)
    state = subNib4(sBoxI, state)
    state = addKey(bitmat((w[2] << 8) + w[3]), state)
    state = MixColumni(state)
    state = shiftRow(state)
    state = subNib4(sBoxI, state)
    state = addKey(bitmat((w[0] << 8) + w[1]), state)
    return matbit(state)
#plaintext = '1101011100101000'
#key = '0100101011110101'
#ciphertext = '0010010011101100'
plaintext = '0110111101101011'
key = '1010011100111011'
ciphertext = '0000011100111000'
w = keyExp(key)
#encrypt(int(plaintext,2))
print('encrypt plaintext = '+ bin(encrypt(int(plaintext,2)))[2:].zfill(16))
print('decrypt ciphertext = '+ bin(decrypt(int(ciphertext,2)))[2:].zfill(16))
