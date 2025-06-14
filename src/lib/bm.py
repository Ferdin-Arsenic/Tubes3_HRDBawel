# File: src/lib/bm.py

def last_occurance(pattern):
    """
    Membuat tabel 'bad character (last_occurance)' menggunakan dictionary untuk mendukung semua karakter (Unicode).
    """
    last_char_table = {}
    pattern_length = len(pattern)
    for i in range(pattern_length):
        last_char_table[pattern[i]] = i
    return last_char_table

def BM(text, pattern):
    """
    Fungsi pencarian string dengan algoritma Boyer-Moore yang sudah diperbaiki
    untuk menangani semua jenis karakter (Unicode).
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or n == 0 or m > n:
        return False

    bad_char_table = last_occurance(pattern)
    shift = 0

    while shift <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return True
        
        else:
            current_char_in_text = text[shift + j]
            
            last_occurrence = bad_char_table.get(current_char_in_text, -1)
            
            shift += max(1, j - last_occurrence)
            
    return False 
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