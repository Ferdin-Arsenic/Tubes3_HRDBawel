def last_occurance(pattern: str) -> dict:
    """
    Membuat tabel 'bad character (last_occurance)' menggunakan dictionary untuk mendukung semua karakter (Unicode).
    """
    last_char_table = {}
    pattern_length = len(pattern)
    for i in range(pattern_length):
        last_char_table[pattern[i]] = i
    return last_char_table

def BM(text: str, pattern: str) -> list[int]:
    """
    Fungsi pencarian string dengan algoritma Boyer-Moore yang sudah diperbaiki
    untuk menangani semua jenis karakter (Unicode) dan mengembalikan semua indeks kemunculan.
    """
    n = len(text)
    m = len(pattern)
    matches = []

    if m == 0 or n == 0 or m > n:
        return matches

    bad_char_table = last_occurance(pattern)
    shift = 0

    while shift <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            matches.append(shift)
            if shift + m < n:
                shift += m - bad_char_table.get(text[shift + m], -1)
            else:
                shift += 1
        
        else:
            # Pattern tidak cocok, lakukan pergeseran berdasarkan 'bad character rule'
            current_char_in_text = text[shift + j]
            last_occurrence = bad_char_table.get(current_char_in_text, -1)
            shift += max(1, j - last_occurrence)
            
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

    text3 = "TRUSTHARDTOOTHBRUSHES"
    pattern3 = "TOOTH"
    matches3 = BM(text3, pattern3)
    print(f"Pattern '{pattern3}' found in '{text3}' at indices: {matches3}")