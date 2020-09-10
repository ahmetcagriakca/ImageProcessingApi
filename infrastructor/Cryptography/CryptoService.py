from cryptography.fernet import Fernet


class CryptoService:
    def __init__(self):
        pass

    @staticmethod
    def decrypt_code(crypted_text):
        key = b's4GGU7jFnKjgu1LsK7fUdxOp1DUSQ-PVgvr28rBNAHM='
        f = Fernet(key)
        return f.decrypt(crypted_text)
