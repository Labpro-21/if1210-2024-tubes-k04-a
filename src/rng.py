import time

def _lcg(a:int, c:int, m: int) -> int:
    """
    Generator Kongruensial Linier (LCG).
    """
    return (a + c) % m
    

def get(a: int, b: int) -> int:
    """
    Menghasilkan angka pseudo-acak dalam rentang [a, b).
    """
    if a > b:
        temp = a
        a = b
        b = temp

    seed = time.time_ns() // 100
    result = a + _lcg(seed, (b - a) // 10, b - a)
    return result

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    for i in range(10):
        print(get(0, 100))

    for i in range(100):
        print(time.time_ns())
