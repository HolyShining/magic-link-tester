from project.aes_cipher import AESCipher

cipher = AESCipher('HeLLo')


def test_encryption():
    plaintext = 'Hello Alberto :)'
    encrypted = cipher.encrypt(plaintext)
    assert len(encrypted) == 64


def test_decryption():
    plaintext = 'Hello Alberto :)'
    encrypted = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(encrypted)
    assert plaintext == decrypted
