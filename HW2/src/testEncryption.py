# Siddhant Shah
# uses python2.7 

# imports
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import timeit
from functools import partial

def main():

    key = "01234567890123456789012345678901";
    iv = "0123456789012345";
    #plainText = "The quick brown fox jumps over the lazy dog";
    plainText = "The quick brown!"

    f = open('pycryptoResults.txt', 'w')

    key1 = RSA.generate(1024)
    key2 = RSA.generate(2048)

    cipher = AES.new(key, AES.MODE_ECB)

    # Timing AES
    
    times = timeit.Timer(partial(cipher.encrypt, plainText)).repeat(10, 1000)
    f.write('AES128 encrypt Time: {0}\n'.format(str(min(times))))

    cipherText = cipher.encrypt(plainText)

    times = timeit.Timer(partial(cipher.decrypt, cipherText)).repeat(10, 1000)
    f.write('AES128 decrypt Time: {0}\n'.format(str(min(times))))

    # Making some byte arrays to hash with SHA256

    arr = ['a'*10**x for x in range(2,7)]

    # Do the hashing

    for plainText in arr:
        times = timeit.Timer(partial(SHA256.new, plainText)).repeat(10, 1000)
        f.write('SHA256 {0} bytes hash Time: {1} \n'.format(len(plainText), min(times)))


    in256 = SHA256.new(arr[1])
    
    # Importing 1024b RSA keys

    publicObj = RSA.importKey(open('public1024.pem').read())
    privateObj = RSA.importKey(open('priv1024.pem').read())

    times = timeit.Timer(partial(publicObj.encrypt, in256.hexdigest(), 4)).repeat(10, 1000)
    f.write('RSA256 1024b Encrypt Time: {0}\n'.format(str(min(times))))

    cipherText = publicObj.encrypt(in256.hexdigest(), 4)

    times = timeit.Timer(partial(privateObj.decrypt, cipherText)).repeat(10, 1000)
    f.write('RSA256 1024b Decrypt Time: {0}\n'.format(str(min(times))))

    # Importing 2048b RSA keys

    publicObj = RSA.importKey(open('public2048.pem').read())
    privateObj = RSA.importKey(open('priv2048.pem').read())

    times = timeit.Timer(partial(publicObj.encrypt, in256.hexdigest(), 4)).repeat(10, 1000)
    f.write('RSA256 2048b Encrypt Time: {0}\n'.format(str(min(times))))

    cipherText = publicObj.encrypt(in256.hexdigest(), 4)

    times = timeit.Timer(partial(privateObj.decrypt, cipherText)).repeat(10, 1000)
    f.write('RSA256 2048b Decrypt Time: {0}\n'.format(str(min(times))))

    return


main()