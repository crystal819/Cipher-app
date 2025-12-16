import random

def encrypt(plain_text, key):
    key = key%26
    encrypted_text = ''
    for character in plain_text: 
        if ord(character) >= 65 and ord(character) <= 90:
            temp = ord(character) + key
            if temp > 90:
                encrypted_text += chr(temp-26)
            else:
                encrypted_text += chr(temp)
        elif ord(character) >= 97 and ord(character) <= 122:
            temp = ord(character) + key
            if temp > 122:
                encrypted_text += chr(temp-26)
            else:
                encrypted_text += chr(temp)
    return encrypted_text

def decrypt(encrypted_text, key):
    key = key%26
    decrypted_text = ''
    for character in encrypted_text:
        if ord(character) >= 65 and ord(character) <= 90:
            temp = ord(character) - key
            if temp < 65:
                decrypted_text += chr(temp+26)
            else:
                decrypted_text += chr(temp)
        elif ord(character) >= 97 and ord(character) <= 122:
            temp = ord(character) - key
            if temp < 97:
                decrypted_text += chr(temp+26)
            else:
                decrypted_text += chr(temp)
    return decrypted_text


def gen_rng_key():
    return random.randint(1, 25)


if __name__ == '__main__':
    choice = input("Do you want do encrypt or decrypt? ")
    if choice == 'encrypt':
        plain_text = input("Enter the plain text you want to encrypt with a caesar cipher: ")
        key = int(input("Enter the key for this text: "))
        encrypted_text = encrypt(plain_text, key)
        print(encrypted_text)
    elif choice == 'decrypt':
        encrypted_text = input("Enter the encrypted text you want to decrypt with a caesar cipher: ")
        key = int(input("Enter the key for this text: "))
        decrypted_text = decrypt(encrypted_text, key)
        print(decrypted_text)
    