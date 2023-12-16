from __future__ import print_function
import random
import math


# # generates a p efficiently and ensures q [(p-1)/2] is a p
# def generate_p(bits):
#     while True:
#         # generate a random odd number of 'bits' length
#         p = random.getrandbits(bits)
#         p |= 2**(bits-1) | 1

#         # check if the number and its q value is p using the Miller-Rabin primality test
#         if is_p(p) and is_p((p-1)/2):
#             return p
  
        
# # checks if a number is p efficiently
# def is_p(n):
#     # check if n is divisible by 2
#     if n == 2 or n == 3:
#         return True
#     if n % 2 == 0:
#         return False

#     # find r and d such that n = 2^r * d + 1
#     r = 0
#     d = n - 1
#     while d % 2 == 0:
#         r += 1
#         d //= 2

#     # test for 'k' random bases using the Miller-Rabin test
#     k = int(math.log(n, 2))  # k = log2(n)
#     for i in range(k):
#         a = random.randint(2, n-2)
#         x = pow(a, d, n)
#         if x == 1 or x == n-1:
#             continue
#         for j in range(r-1):
#             x = pow(x, 2, n)
#             if x == n-1:
#                 break
#         else:
#             return False

#     return True

# # generates a generator for previously generated p (method used is from a lemma)
# def generate_g(p):
#     q = (p-1)/2 
#     # pick a g to start
#     g = random.randint(2, p-1)
    
#     # following condition is based on a lemma we learned in class
#     while pow(g, 1, p) == 1 or pow(g, 2, p) == 1 or pow(g, q, p) == 1:
#         g = random.randint(2, p-1)
#     return g


# to find if an inverse exists
def gcd(a, b):
    if a < b:
        a, b = b, a     # swap a and b so a is larger
    while b != 0:       # loop until b is 0, then we have found gcd
        a, b = b, a % b     # a is now b and b is now a % b
    return a  


# pulverizer/extended Euclidean algo
def pulverizer(a, b):
    # basis
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = pulverizer(b % a, a)
    
    # update x and y after recursive calls
    x = y1 - (b//a) * x1
    y = x1
 
    return gcd, x, y

# converts plain text into ascii characters
def to_ascii_str(text):
    ascii_txt = ''
    for character in text:
        ascii_txt+= str(ord(character)) + '\n'
        
    return ascii_txt

# encryption method
def encrypt_num(m, p, g, b):
    n = random.randint(1, p-2)
    k = pow(b, n, p) # for salting
    
    h = pow(g, k, p) # half mask
    part_cipher = pow(h, a, p)
    
    # y = (m*k) % p ---- this was not giving me the right cipher value so i 
    # went back, found an error when going through the encryption/decryption formulas,
    # and fixed my formula in order have the terms in the decryption formula cancel & give the msg
    y = (int(m)*part_cipher) % p # cipher
    return pow(g, k, p), y # returns half mask, cipher

# decryption method
def decrypt_num(h, y, a, p):
    f = pow(int(h), a, p)
    _, _, invf = pulverizer(p, f)
    msg = (int(y) * invf) % p
    return chr(msg)
    


# asking for user input (bit length and file names)
# bit_length = int(raw_input("Enter the bit length for the primes: "))
plain_name = raw_input("Enter the plain text file name (with .txt): ")
plain_file = open(plain_name, "r")
cipher_name = raw_input("Enter a cipher text file name (with .txt): ")
cipher_file = open(cipher_name, "w+")
ascii_msg = to_ascii_str(plain_file.read())

# # keys to randomly generate values (program slows down at >250 bits)
# p = generate_p(bit_length) 
# g = generate_g(p) 
# b = random.randint(0, p-1)
# a = random.randint(0, p-1)


p = 38072042136930207360134700552835279982042792835496840050682579327442579766193
g = pow(2, 38072042136930207360134700552835279982042792835496840050682579327442579766192, p)
b = 23398739824798234798234798234798237498
a = 29810385192055033015150804063543289102470154663169901719256685801461416657483

# # put keys in a file
# keys = open("elgamal_keys.txt", "w+")
# keys.write("p = " + str(p) + "\n")
# keys.write("g = " + str(g) + "\n")
# keys.write("b = " + str(b) + "\n")
# keys.write("a = " + str(a) + "\n")


# encrypt msg and write the half_mask-cipher pair into a file
for m in ascii_msg.splitlines(): 
    h, y = encrypt_num(m, p, g, b)
    cipher_file.write(str(h) + '   ' + str(y) + '\n')
 
print()
   
cipher_file.seek(0) # back to beginning of file for reading
for line in cipher_file.read().splitlines():
    h, _, y = line.partition('   ')
    # print decrypted msg to terminal
    print(decrypt_num(h, y, a, p), end ="")   

print("\n")
