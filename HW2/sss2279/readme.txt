To run my code, cd into the src directory. Then:

To run OpenSSL:

g++ testEncryption.cpp -o testEncryption.o -ggdb -g -fpermissive -lcrypto && ./testEncryption.o

To run PycryptoDome:

python testEncryption.py

To run testRNG:

python3 testRNG.py
