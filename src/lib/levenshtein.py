def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Menghitung Levenshtein Distance antara dua string.

    Jarak ini adalah jumlah minimum operasi edit (penyisipan, 
    penghapusan, atau substitusi) yang dibutuhkan untuk mengubah
    string s1 menjadi s2.
    """
    m, n = len(s1), len(s2)

    # Inisialisasi matriks DP (Dynamic Programming)
    # dp[i][j] akan menjadi jarak antara i karakter pertama s1
    # dan j karakter pertama s2.
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Inisialisasi baris dan kolom pertama
    # Jarak dari string kosong ke string lain adalah panjang string itu sendiri
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Mengisi matriks DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1  # Biaya substitusi
            dp[i][j] = min(dp[i - 1][j] + 1,        # Deletion
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution
    return dp[m][n]

if __name__ == "__main__":
    # Contoh 1: kitten -> sitting (3 operasi)
    # 1. k -> s (substitusi)
    # 2. e -> i (substitusi)
    # 3.   -> g (penyisipan)
    s1 = "kitten"
    s2 = "sitting"
    distance = levenshtein_distance(s1, s2)
    print(f"Levenshtein distance between '{s1}' and '{s2}' is: {distance}") # Expected: 3

    # Contoh 2: Saturday -> Sunday (3 operasi)
    # 1. S'at'urday -> S'un'day
    s1 = "Saturday"
    s2 = "Sunday"
    distance = levenshtein_distance(s1, s2)
    print(f"Levenshtein distance between '{s1}' and '{s2}' is: {distance}") # Expected: 3

    # Contoh 3: String yang sama
    s1 = "python"
    s2 = "python"
    distance = levenshtein_distance(s1, s2)
    print(f"Levenshtein distance between '{s1}' and '{s2}' is: {distance}") # Expected: 0

    # Contoh 4: String yang sangat berbeda
    s1 = "algorithm"
    s2 = "levenshtein"
    distance = levenshtein_distance(s1, s2)
    print(f"Levenshtein distance between '{s1}' and '{s2}' is: {distance}") # Expected: 10