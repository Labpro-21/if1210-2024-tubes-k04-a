# SEED berisi karakter-karakter yang digunakan sebagai basis enkripsi dan dekripsi
SEED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|`~:;'<>?\",.1234567890/"

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
    option = input("encrypt or decrypt? ")
    if option == "encrypt":
        text = input("Insert text to be encrypted: ")
        print("encrypted: ", encrypt(text))
    elif option == "decrypt":
        text = input("Insert text to be decrypted: ")
        print("decrypted: ", decrypt(text))
    else:
        print("Please input 'encrypt' or 'decrypt'")

    

