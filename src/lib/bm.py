def bad_char_heuristic(pattern: str, size: int) -> list[int]:
    """
    Preprocessing untuk menghasilkan tabel Bad Character.
    Tabel ini menyimpan kemunculan terakhir dari setiap karakter dalam pola.
    """
    bad_char = [-1] * 256  

    # Isi nilai kemunculan terakhir dari karakter yang ada di pola
    for i in range(size):
        bad_char[ord(pattern[i])] = i
        
    return bad_char

def BM(text: str, pattern: str) -> list[int]:
    """
    Algoritma Boyer-Moore (BM) untuk pencarian substring.

    Mencari kemunculan pasti dari sebuah pola dalam teks.
    Menggunakan heuristik 'Bad Character' untuk mempercepat pencarian.
    Mengembalikan daftar indeks awal di mana pola ditemukan dalam teks.
    """
    matches = []
    m = len(pattern)
    n = len(text)

    if m == 0 or n == 0 or m > n:
        return []

    bad_char = bad_char_heuristic(pattern, m)
    
    s = 0  #SHIFT
    while(s <= n - m):
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            matches.append(s)

            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
            
    return matches

if __name__ == "__main__":
    text = "BILAKATADARIKATAMANAKATAKATA"
    pattern = "KATA"
    matches = BM(text, pattern)
    print(f"Pattern '{pattern}' found in '{text}' at indices: {matches}")

    text2 = "ABABDABACDABABCABAB"
    pattern2 = "ABABCABAB"
    matches2 = BM(text2, pattern2)
    print(f"Pattern '{pattern2}' found in '{text2}' at indices: {matches2}")

    # Contoh yang menyoroti kekuatan Boyer-Moore (lompatan besar)
    text3 = "TRUSTHARDTOOTHBRUSHES"
    pattern3 = "TOOTH"
    matches3 = BM(text3, pattern3)
    print(f"Pattern '{pattern3}' found in '{text3}' at indices: {matches3}")