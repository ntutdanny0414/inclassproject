#testcase
#key = "0111111101"
#cipher = "10100010"
#plaint = "11101010"

#key = "1100011110"
#cipher = "10001010"
#plaint = "00101000"

#permutation way
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
P4 = (2, 4, 3, 1)
IP = (2, 6, 3, 1, 4, 8, 5, 7)
IPi = (4, 1, 3, 5, 7, 2, 8, 6)
E = (4, 1, 2, 3, 2, 3, 4, 1)
# sbox
S0 = [
      [1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]
     ]
S1 = [
      [0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]
     ]
def permutation(way, key):
    permutated_out = ""
    for i in way:
        permutated_out += key[i-1]
    return permutated_out
#shift way
def shift_first_key(left_key, right_key):
    left_key_per = left_key[1:] + left_key[:1]
    right_key_per = right_key[1:] + right_key[:1]
    shift_key = left_key_per + right_key_per
    return shift_key
def shift_second_key(left_key, right_key):
    left_key_per = left_key[2:] + left_key[:2]
    right_key_per = right_key[2:] + right_key[:2]
    shift_key = left_key_per + right_key_per
    return shift_key
#FK#zfill補齊
def FK(after_IP_left,after_IP_right, key):
    E_per = permutation(E, after_IP_right)
    xor_cipher_one = bin(int(E_per, 2) ^ int(key, 2))[2:].zfill(8)#XOR
#    print(xor_cipher_one)
    left_xor_cipher = xor_cipher_one[:4]
    right_xor_cipher = xor_cipher_one[4:]
    #sbox
    left_sbox_cipher = Sbox(left_xor_cipher, S0)
    right_sbox_cipher = Sbox(right_xor_cipher, S1)
    P4_per = permutation(P4, left_sbox_cipher + right_sbox_cipher)
    xor_cipher_two = int(after_IP_left, 2) ^ int(P4_per, 2)
    return bin(xor_cipher_two)[2:].zfill(4) , after_IP_right
#sbox
def Sbox(after_xor_one, sbox):
    row = int(after_xor_one[0] + after_xor_one[3], 2)
    col = int(after_xor_one[1] + after_xor_one[2], 2)
    return bin(sbox[row][col])[2:].zfill(2)#change2bit
# encrypt
def encrypt(plaintext,first_key,second_key):
    #IP
    IP_per = permutation(IP, plaintext)
    after_IP_left = IP_per[:int(len(IP_per)/2)]
    after_IP_right = IP_per[int(len(IP_per)/2):]
    #FK
    FK_one_left , FK_one_right = FK(after_IP_left, after_IP_right, first_key)
    #SW
    SW_left , SW_right = FK_one_right , FK_one_left
    #FK_AGAIN
    FK_two_left , FK_two_right = FK(SW_left, SW_right, second_key)#second_key
    #IPi
    return permutation(IPi, FK_two_left + FK_two_right)
#decrypt
def decrypt(ciphertext,first_key,second_key):
    #IP
    IP_per = permutation(IP, ciphertext)
    after_IP_left = IP_per[:int(len(IP_per)/2)]
    after_IP_right = IP_per[int(len(IP_per)/2):]
    #FK
    FK_one_left , FK_one_right = FK(after_IP_left, after_IP_right, second_key)#second_key_start
    #SW
    SW_left , SW_right = FK_one_right , FK_one_left
    #FK_AGAIN
    FK_two_left , FK_two_right = FK(SW_left, SW_right, first_key)
    #IPi
    return permutation(IPi, FK_two_left + FK_two_right)    
# generatekey
def generate_key(key):
    p10_per = permutation(P10, key)
    left = p10_per[:int(len(p10_per)/2)]
    right = p10_per[int(len(p10_per)/2):]
    #shift_one
    shift = shift_first_key(left, right)
    #key1
    first_key = permutation(P8,shift)
    #shift_two
    shift_second = shift_second_key(shift[:int(len(shift)/2)], shift[int(len(shift)/2):])
    #key2
    second_key = permutation(P8,shift_second)
    return first_key,second_key
def main():
    func = input('encrypt-1 , decrypt-2: ')
    key = input('key = ')#string
    # generatekey
    first_key,second_key = generate_key(key)[0],generate_key(key)[1]
    if func == '1':
        plaintext = input('plaintext(8bit): ')
        print('ciphertext: ' + encrypt(plaintext,first_key,second_key))
    elif func == '2':
        ciphertext = input('ciphertext(8bit): ')
        print('plaintext: ' + decrypt(ciphertext,first_key,second_key))
main()
