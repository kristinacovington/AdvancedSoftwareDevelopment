from Crypto.PublicKey import RSA
from Crypto.Cipher import DES

block_size = 8

def pad(text):
    return text + ((block_size - len(text) % block_size) * chr(block_size - len(text) % block_size)).encode()

#Unpadding code from stackoverflow
def unpad(s):
    return s[:-ord(s[len(s) - 1:])]

def make_key(key):
    if isinstance(key, DES.DESCipher):
        return key
    else:
        keystr = str(key).encode()
        if len(keystr) < 8:
            keystr = pad(keystr)
        elif len(keystr) > 8:
            keystr = keystr[:8]
        keyobj = DES.new(keystr)
        return keyobj

def encrypt_string(plaintext, key):
    key = make_key(key)
    try:
        if not isinstance(plaintext, bytes):
            raise TypeError('plaintext must be bytes')
        if not isinstance(key, DES.DESCipher):
            raise TypeError('key is not a valid key')
    except TypeError as e:
        print(e.args[0])
        print('Try again')
        return ""

    plaintext = pad(plaintext)
    ciphertext = key.encrypt(plaintext)

    return ciphertext

def decrypt_string(ciphertext, key):
    key = make_key(key)
    try:
        if not isinstance(ciphertext, bytes):
            raise TypeError('ciphertext must be a bytes')
        if not isinstance(key, DES.DESCipher):
            raise TypeError('key is not a valid key')
    except TypeError as e:
        print(e.args[0])
        print('Try again')
        return ""

    plaintext = key.decrypt(ciphertext)
    plaintext = unpad(plaintext)

    return plaintext



def encrypt_file(filename, key):
    key = make_key(key)
    try:
        if not isinstance(filename, str):
            raise TypeError('filename must be a string')
        if not isinstance(key, DES.DESCipher):
            raise TypeError('key is not a DES key')
        f = open(filename, 'rb')
    except TypeError as e:
        print(e.args[0])
        print('Try again')
        return False
    except FileNotFoundError as e:
        print(e.args[0])
        print('Try again')
        return False

    data = f.read()
    f.close()
    data = pad(data)
    cipher = key.encrypt(data)

    try:
        new_file = filename + ".enc"
        f = open(new_file, 'wb')
    except FileNotFoundError as e:
        print(e.args)
        return False

    f.write(cipher)
    f.close()
    return True

def decrypt_file(filename, key):
    key = make_key(key)

    try:
        if not isinstance(filename, str):
            raise TypeError('filename must be a string')
        if not isinstance(key, DES.DESCipher):
            raise TypeError('key is not a DES key')
        f = open(filename, 'rb')
    except TypeError as e:
        print(e.args[0])
        print('Try again')
        return False
    except FileNotFoundError as e:
        print(e.args[0])
        print('Try again')
        return False

    cipher = f.read()
    f.close()
    plain = key.decrypt(cipher)
    raw = unpad(plain)

    filename = filename[:-4]
    try:
        new_file = "DEC_" + filename
        f = open(new_file, 'wb')
    except FileNotFoundError as e:
        print(e.args)
        return False

    f.write(raw)
    f.close()
    return True


if __name__ == "__main__":
    pass


