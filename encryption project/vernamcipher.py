import random

def encrypt(plain_text, key): #str, str
    encrypted_text = ''
    for i in range(0, len(plain_text)):
        hex_val = hex(ord(plain_text[i]) ^ ord(key[i%len(key)]))[2:]
        if len(hex_val) == 1:
            hex_val = '0' + hex_val
        if len(hex_val) == 2:
                encrypted_text += hex_val 
    return encrypted_text

def decrypt(encrypted_text, key): #str, str
    decrypted_text = ''
    for i in range(1, len(encrypted_text), 2):
            hex_val = str(encrypted_text[i-1]) + str(encrypted_text[i])
            decrypted_text += chr(ord(key[int(((i-1)/2)%len(key))]) ^ int(hex_val, 16))
    return decrypted_text


def gen_rng_key(input_txt):
    if type(input_txt) == str:
        len_word = len(input_txt)
    elif type(input_txt) == int:
        len_word = input_txt

    if len_word == 0:
        len_word = 10
        
    random_word = ''
    for _ in range(len_word):
        random_word += chr(random.randint(97, 122))
    return random_word
          

if __name__ == '__main__':
    choice = input("Do you want do encrypt or decrypt? ")
    if choice == 'encrypt':
        plain_text = input("Enter the plain text you want to encrypt using the vernam cipher: ")
        key = input("Enter the key you want to use (best to use one the same long as the text): ")
        encrypted_text = encrypt(plain_text, key)
        print(encrypted_text)
    elif choice == 'decrypt':
        encrypted_text = input("Enter the encrypted text you want to decrypt using the vernam cipher: ")
        key = input("Enter the key you want to use (best to use one the same long as the text): ")
        decrypted_text = decrypt(encrypted_text, key)
        print(decrypted_text)
    