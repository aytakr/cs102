def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in range(0, len(plaintext)):
        if ord("A") <= ord(plaintext[i]) <= ord("Z"):
            a = ord("A")
            ciphertext += chr((ord(plaintext[i]) + 3 - a) % 26 + a)
        elif ord("a") <= ord(plaintext[i]) <= ord("z"):
            a = ord("a")
            ciphertext += chr((ord(plaintext[i]) + 3 - a) % 26 + a)
        else:
            ciphertext += plaintext[i]
    return ciphertext

    
def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in range(0, len(ciphertext)):
        if ord("A") <= ord(ciphertext[i]) <= ord("Z"):
            a = ord("A")
            plaintext += chr((ord(ciphertext[i]) - 3 - a) % 26 + a)
        elif ord("a") <= ord(ciphertext[i]) <= ord("z"):
            a = ord("a")
            plaintext += chr((ord(ciphertext[i]) - 3 - a) % 26 + a)
        else:
            plaintext += ciphertext[i]
    return plaintext
