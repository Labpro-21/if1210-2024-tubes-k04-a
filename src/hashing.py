# SEED berisi karakter-karakter yang digunakan sebagai basis enkripsi dan dekripsi
SEED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|`~:;'<>?\",. 1234567890/\\"

def encrypt(text: str) -> str:
    """
    Mengenkripsi teks menggunakan algoritm Caesar Cipher yang sedikit dimodifikasi sehingga pergeseran menyesuaikan dengan posisi karakter pada teks.
    """
    encrypted = ""

    for i in range(len(text)):
        for j in range(len(SEED)):
            if SEED[j] == text[i]:
                encrypted += SEED[(j + i + 1) % len(SEED)]
                break

    return encrypted

def decrypt(text: str) -> str:
    """
    Mendekripsi teks yang telah dienkripsi.
    """
    decrypted = ""

    for i in range(len(text)):
        for j in range(len(SEED)):
            if SEED[j] == text[i]:
                decrypted += SEED[(j - i - 1 + len(SEED)) % len(SEED)]
                break

    return decrypted

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    text = input("Input text: ")

    enc = encrypt(text)
    print("encrypted: ", enc)
    dnc = decrypt(enc)
    print("decrypted: ", dnc)
    

