import os
import sys
from optparse import OptionParser

'''
My implementation of CipherSaber-2 from ciphersaber.gurus.org
'''

def key_setup(key, num_loops=20):
    # ARCFOUR 3.1
    
    S = []
    keylen = len(key)
    
    # Initialize state (S) and key arrays (S2)
    for i in range(0,256):
        S.append(i)
    
    # Mixing loop
    j = 0
    for loopnum in range(0,num_loops):
        for i in range(0,256):
            j = (j + S[i] + ord(key[i % keylen])) % 256
            S[i], S[j] = S[j], S[i]
    
    # Playing it safe
    i = 0
    j = 0
    key = ''
    
    return S
    
def cipher(S, data):
    # ARCFOUR 3.2
    
    i = 0
    j = 0
    stream = ''
    
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        n = (S[i] + S[j]) % 256
        stream += chr(S[n] ^ ord(byte))
    
    # Playing it safe
    S = []
        
    return stream
    
    
def encrypt(key, plaintext, num_loops=20):
    # Mix the key, add the IV and return the encrypted data
    
    iv = os.urandom(10)  # Initialization vector (IV)
    S = key_setup(key+iv, num_loops)
    ciphertext = iv + cipher(S, plaintext)
    return ciphertext
    
def decrypt(key, ciphertext, num_loops=20):
    # Mix the key, strip the IV and return unencrypted data
    
    iv = ciphertext[:10]
    S = key_setup(key+iv, num_loops)
    stripped = ciphertext[10:]  # Strip the IV
    plaintext = cipher(S, stripped)
    return plaintext

def main():
    parser = OptionParser(usage='usage: %prog [options] FILE KEY')
    parser.set_defaults(encrypt=True)
    parser.add_option('-e', '--encrypt', action='store_true', 
                      dest='encrypt', help='Encrypt FILE (default)')
    parser.add_option('-d', '--decrypt', action='store_false', 
                      dest='encrypt', help='Decrypt FILE')
    parser.add_option('-n', type='int', dest='num_loops', default=20,
                      help='Number of times to mix the state array (default: %default)')
    
    (options, args) = parser.parse_args()
    
    if len(args) != 2:
        parser.error('Please specify exactly two arguments.')
        
    with open(args[0], 'rb') as f:
        if options.encrypt == True:
            sys.stdout.write(encrypt(args[1], f.read(), options.num_loops))
        if options.encrypt == False:
            sys.stdout.write(decrypt(args[1], f.read(), options.num_loops))
            

if __name__ == '__main__':
    main()