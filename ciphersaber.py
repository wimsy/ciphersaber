import os

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

