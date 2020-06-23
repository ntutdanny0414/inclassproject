# -*- coding: utf-8 -*-
import math
def affine_Caesar(a,b,letter):
    cipher = (a * (ord(letter) - 65) + b) % 26 # A ascll = 65
    cipherletter = chr(cipher+65)#+65
    return cipherletter
def Brute_Force(a,b,letter):#暴力破解
    for i in range(26):
        if affine_Caesar(a,b,chr(i+65)) == letter:
            return chr(i+65)
def encrypt(a,b,plaintext):
    outcome = ''
    for i in range(0,len(plaintext)):
        outcome = outcome + affine_Caesar(a,b,plaintext[i])
    return outcome
def decrypt(a,b,ciphertext):
    outcome = ''
    for i in range(0,len(ciphertext)):
        outcome = outcome + Brute_Force(a,b,ciphertext[i])
    return outcome
def main():
    func = input('encrypt-1 , decrypt-2: ')
    a = int(input('a = '))
    b = int(input('b = '))
    if math.gcd(a,26) == 1:#判斷互質
        if func == '1':
            plaintext = input('plaintext(A-Z): ').upper()# 以大寫英文為主
            print('ciphertext: '+encrypt(a,b,plaintext))
        elif func == '2':
            ciphertext = input('ciphertext(A-Z): ').upper()
            print('plaintext: '+decrypt(a,b,ciphertext))
    else:
        print('a is not allow!')
main()
