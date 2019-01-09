// g++ testEncryption.cpp -o testEncryption.o -ggdb -g -fpermissive -lcrypto && ./testEncryption.o 


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <ctime>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/rsa.h>
#include <openssl/sha.h>
#include <openssl/pem.h>
#include <openssl/bio.h>

#include <openssl/objects.h>
#include <openssl/x509.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/ssl.h>
#include <openssl/engine.h>
#include <openssl/rand.h>


double encryptAES128(EVP_CIPHER_CTX *ctx, unsigned char* plainText, unsigned char* cipherText, int* plainText_len, int* cipherText_len );
double decryptAES128(EVP_CIPHER_CTX *ctx, unsigned char* cipherText, unsigned char* decryptedText, int* plainText_len, int* cipherText_len);
double hashSHA256(int numBytes, unsigned char* rands);
double encryptRSA256(unsigned char* plainText, unsigned char* cipherText, RSA* keypair);
double decryptRSA256(unsigned char* cipherText, unsigned char* decryptedText, RSA* keypair);
void handleErrors(void);
int* password(char* a, int b, int c, void* d)
{
  return (int)* "walrus";
  //return (int)* "whales";
}


int main(int arc, char *argv[])
{ 
  /* Set up the key and iv. Do I need to say to not hard code these in a
   * real application? :-)
   */

  /* A 256 bit key */
  unsigned char *key = (unsigned char *)"01234567890123456789012345678901";

  /* A 128 bit IV */
  unsigned char *iv = (unsigned char *)"0123456789012345";

  /* Message to be encrypted */
  unsigned char *plainText =
                (unsigned char *)"The quick brown fox jumps over the lazy dog";

  EVP_CIPHER_CTX *ctx;

  /* Create and initialise the conText */
  int cipherText_len;
  int plainText_len;
  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();
  if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, iv))
    handleErrors();
  if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, iv))
    handleErrors();

  //BIO* = BIO_new(BIO_f_base64());

  //RSA *keypair_1024 = RSA_generate_key(1024, 3, NULL, NULL);
  //RSA *keypair_2048 = RSA_generate_key(2048, 3, NULL, NULL);

  RSA* a = RSA_new();

  FILE* f1 = fopen("public1024.pem", "r");
  FILE* f2 = fopen("priv1024.pem", "r");
  FILE* f3 = fopen("public2048.pem", "r");
  FILE* f4 = fopen("priv2048.pem", "r");

  RSA *public1024 = PEM_read_RSA_PUBKEY(f1, NULL, NULL, NULL);
  RSA *private1024 = PEM_read_RSAPrivateKey(f2, NULL, password, NULL);
  RSA *public2048 = PEM_read_RSA_PUBKEY(f3, &a, NULL, NULL);
  RSA *private2048 = PEM_read_RSAPrivateKey(f4, NULL, password, NULL);
  /* Buffer for cipherText. Ensure the buffer is long enough for the
   * cipherText which may be longer than the plainText, dependant on the
   * algorithm and mode
   */
  unsigned char cipherText[128];

  /* Buffer for the decrypted Text */
  unsigned char decryptedText[128];

  // for RSA
  const unsigned char randomBytes[256];
  unsigned char cipherText2[256];
  unsigned char decryptedText2[256];

  double aes128enc = 0;
  double aes128dec = 0;
  double sha256_1e2 = 0;
  double sha256_1e3 = 0;
  double sha256_1e4 = 0;
  double sha256_1e5 = 0;
  double sha256_1e6 = 0;
  double rsa256enc_1024b = 0;
  double rsa256dec_1024b = 0;
  double rsa256enc_2048b = 0;
  double rsa256dec_2048b = 0;

  for (int i = 0; i < 10000; i++)
  {
    
    aes128enc += encryptAES128(ctx, plainText, cipherText, &plainText_len, &cipherText_len);
    aes128dec += decryptAES128(ctx, cipherText, decryptedText, &plainText_len, &cipherText_len);
    
    //std::cout << "AES OK \n";
    sha256_1e2 += hashSHA256(100, randomBytes);
    sha256_1e3 += hashSHA256(1000, randomBytes);
    sha256_1e4 += hashSHA256(10000, randomBytes);
    sha256_1e5 += hashSHA256(100000, randomBytes);
    sha256_1e6 += hashSHA256(1000000, randomBytes);
    //std::cout << "SHA OK \n";
    rsa256enc_1024b += encryptRSA256(randomBytes, cipherText2, public1024);
    rsa256dec_1024b += decryptRSA256(cipherText2, decryptedText2, private1024);
    rsa256enc_2048b += encryptRSA256(randomBytes, cipherText2, public2048);
    rsa256dec_2048b += decryptRSA256(cipherText2, decryptedText2, private2048);
    //std::cout << "RSA OK \n";
  }
  EVP_CIPHER_CTX_free(ctx);

  std::cout << "ALL DONE\n";
  FILE* myfile = fopen("opensslResults.txt", "w");
  
  fprintf(myfile, "AES128 Encrypt Time: %.7f\n", aes128enc/10.0); //give time in ms
  fprintf(myfile, "AES128 Decrypt Time: %.7f\n", aes128dec/10.0);
  fprintf(myfile, "SHA256 1e2 Bytes Hash Time: %.7f\n", sha256_1e2/10.0);
  fprintf(myfile, "SHA256 1e3 Bytes Hash Time: %.7f\n", sha256_1e3/10.0);
  fprintf(myfile, "SHA256 1e4 Bytes Hash Time: %.7f\n", sha256_1e4/10.0);
  fprintf(myfile, "SHA256 1e5 Bytes Hash Time: %.7f\n", sha256_1e5/10.0);
  fprintf(myfile, "SHA256 1e6 Bytes Hash Time: %.7f\n", sha256_1e6/10.0);
  fprintf(myfile, "RSA256 1024b-key Encrypt Time: %.7f\n", rsa256enc_1024b/10.0);
  fprintf(myfile, "RSA256 1024b-key Decrypt Time: %.7f\n", rsa256dec_1024b/10.0);
  fprintf(myfile, "RSA256 2048b-key Encrypt Time: %.7f\n", rsa256enc_2048b/10.0);
  fprintf(myfile, "RSA256 2048b-key Decrypt Time: %.7f\n", rsa256dec_2048b/10.0);

  return 0;
}

double encryptAES128(EVP_CIPHER_CTX *ctx, unsigned char* plainText, unsigned char* cipherText, int* plainText_len, int* cipherText_len)
{
  

  /* Encrypt the plainText */

  int len;
  /* Provide the message to be encrypted, and obtain the encrypted output.
   * EVP_EncryptUpdate can be called multiple times if necessary
   */
  double start = std::clock();
  if(1 != EVP_EncryptUpdate(ctx, cipherText, &len, plainText, *plainText_len))
    handleErrors();
  double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
  *cipherText_len = len;
  /* Finalise the encryption. Further cipherText bytes may be written at
   * this stage.
   */
  if(1 != EVP_EncryptFinal_ex(ctx, cipherText + len, &len)) handleErrors();
  *cipherText_len += len;
  /* Do something useful with the cipherText here */
  //printf("CipherText is:\n");
  //BIO_dump_fp (stdout, (const char *)cipherText, cipherText_len);

  /* Decrypt the cipherText */
  return duration;
  
}

double decryptAES128(EVP_CIPHER_CTX *ctx, unsigned char* cipherText, unsigned char* decryptedText, int* plainText_len, int* cipherText_len)
{
  
  int len;
  /* Provide the message to be decrypted, and obtain the plainText output.
   * EVP_DecryptUpdate can be called multiple times if necessary
   */
  double start = std::clock();
  if(1 != EVP_DecryptUpdate(ctx, decryptedText, &len, cipherText, *cipherText_len))
    handleErrors();
  double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
  *plainText_len = len;
  /* Finalise the decryption. Further plainText bytes may be written at
   * this stage.
   */
  if(1 != EVP_DecryptFinal_ex(ctx, decryptedText + len, &len)) handleErrors();
  *plainText_len += len;
  
  /* Add a NULL terminator. We are expecting printable Text */
  //decryptedText[decryptedText_len] = '\0';

  /* Show the decrypted Text */
  /*
  printf("Decrypted Text is:\n");
  printf("%s\n", decryptedText);
  */
  return duration;
}

double hashSHA256(int numBytes, unsigned char* rands)
{
  unsigned char digest[32];
  int num = numBytes / 32 + 1;
  double start = std::clock();
  for (int i = 0; i < num; i++)
  {
    SHA256((unsigned char*)&rands, strlen(rands), (unsigned char*)&digest); 
  }   
  double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
  return duration;

}

double encryptRSA256(unsigned char* plainText, unsigned char* cipherText, RSA* keypair)
{

  double start = std::clock();
  RSA_public_encrypt(32, (unsigned char*)plainText,
   (unsigned char*)cipherText, keypair, RSA_PKCS1_OAEP_PADDING);
  double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
  return duration;

}

double decryptRSA256(unsigned char* cipherText, unsigned char* decryptedText, RSA* keypair)
{
  int encrypt_len;
  double start = std::clock();
  RSA_private_decrypt(32, (unsigned char*)cipherText, (unsigned char*)decryptedText,
                       keypair, RSA_PKCS1_OAEP_PADDING);
  double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
  return duration;
}




void handleErrors(void)
{
  return;
}

