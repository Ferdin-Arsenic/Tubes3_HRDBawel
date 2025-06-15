def borderFunction(pattern: str) -> list[int]:
    # Returns the border function for the givern pattern.
    m = len(pattern)
    border = [0] * m
    j = 0  # length of previous longest prefix suffix

    for i in range(1, m):
        while (j > 0 and pattern[i] != pattern[j]):
            j = border[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        border[i] = j

    return border

def KMP(text: str, pattern: str) -> list[int]:
    """    Knuth-Morris-Pratt (KMP) algorithm for substring search.
    
    Searches for exact occurences of a pattern in the text.
    Returns a list of starting indices where the pattern is found in the text.

    """

    matches = []
    n = len(text)
    m = len(pattern)
    if m == 0:
        return []
    if n == 0 or m > n:
        return []
    
    border = borderFunction(pattern)
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            matches.append(i - j)
            j = border[j - 1] 
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = border[j - 1]
            else:
                i += 1
    return matches


if __name__ == "__main__":
    text = "BILAKATADARIKATAMANAKATAKATA"
    pattern = "KATA"
    matches = KMP(text, pattern)
    print(f"Pattern found at indices: {matches}")

    text2 = "ABABDABACDABABCABAB"
    pattern2 = "ABABCABAB"
    matches2 = KMP(text2, pattern2)
    print(f"Pattern found at indices: {matches2}")

    text3 = "ABZCDEFGHIJKLMNOPQRSTUVWXYMZ"
    pattern3 = "XYZ"
    matches3 = KMP(text3, pattern3)
    print(f"Pattern found at indices: {matches3}")