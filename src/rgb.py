def rgb_text(r, g, b):
  """
  RGB text
  """
  return f"\033[38;2;{r};{g};{b}m"

def rgb_bg(r, g, b):
  """
  RGB background
  """
  return f"\033[48;2;{r};{g};{b}m"

if __name__ == "__main__": # Hanya akan dieksekusi jika dijalankan secara langsung dan bukan sebagai modul
    red = rgb(255, 0, 0)
    green_background = rgb_bg(0, 255, 0)
    reset = "\033[0m" # pastikan SELALU menaruh reset diakhir agar teks kembali menjadi putih

    # Untuk melihat kode warna bisa dicari 

    print(f"{red}{green_background}ini merah dengan background hijau{reset}")