import s_des #sdes額外檔案
IV = '10101010'
plaintext = '0000000100100011'
key = '0111111101'
ciphertext = '1111010000001011'

def encrypt(plaintext,IV,key):
    iv = IV
    ciphertext = ''
    for i in range(len(plaintext)//8):
        xor = bin(int(plaintext[:8],2) ^ int(iv,2))[2:].zfill(8)
        ciphertext = ciphertext + s_des.encrypt(xor,s_des.generate_key(key)[0],s_des.generate_key(key)[1])
        iv = s_des.encrypt(xor,s_des.generate_key(key)[0],s_des.generate_key(key)[1])
        plaintext = plaintext[8:]
    return ciphertext
def decrypt(ciphertext,IV,key):  
    iv = IV
    plaintext = ''
    for i in range(len(ciphertext)//8):
        output = s_des.decrypt(ciphertext[:8],s_des.generate_key(key)[0],s_des.generate_key(key)[1])
        xor = bin(int(output,2) ^ int(iv,2))[2:].zfill(8)
        plaintext = plaintext + xor
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
    return plaintext

print('encrypt plaintext = '+ encrypt(plaintext,IV,key))
print('decrypt ciphertext = '+ decrypt(ciphertext,IV,key))