def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range (0, len(plaintext)):
        j = i % len(keyword)
        if ord("A") <= ord(plaintext[i]) <= ord("Z"):
            ciphertext += chr((ord(plaintext[i]) + ord(keyword[j]) - 2*ord("A")) % 26 + ord("A"))
        elif ord("a") <= ord(plaintext[i]) <= ord("z"):
            ciphertext += chr((ord(plaintext[i]) + ord(keyword[j]) - 2*ord("a")) % 26 + ord("a"))
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range (0, len(ciphertext)):
        j = i % len(keyword)
        if ord("A") <= ord(ciphertext[i]) <= ord("Z"):
            plaintext += chr((ord(ciphertext[i]) - ord(keyword[j])) % 26 + ord("A"))
        elif ord("a") <= ord(ciphertext[i]) <= ord("z"):
            plaintext += chr((ord(ciphertext[i]) - ord(keyword[j])) % 26 + ord("a"))
        else:
            plaintext += ciphertext[i]
    return plaintext
