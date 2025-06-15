from collections import deque

def build_trie(patterns: list[str]) -> tuple[list[dict], list[list[str]]]:
    """
    Membangun struktur Trie dari daftar pola (patterns).
    Struktur ini juga dikenal sebagai 'goto function' dalam Aho-Corasick.

    Returns:
        goto (list[dict]): Transisi state. goto[state][char] -> next_state.
        output (list[list[str]]): Daftar pola yang berakhir di setiap state.
    """
    # Inisialisasi root node (state 0)
    goto = [{'': 0}]  # List of dictionaries, index is the state
    output = [[]]    # List of lists, index is the state
    new_state = 0

    for pattern in patterns:
        state = 0
        for char in pattern:
            if char not in goto[state]:
                new_state += 1
                goto.append({})
                output.append([])
                goto[state][char] = new_state
            state = goto[state][char]
        output[state].append(pattern)
        
    return goto, output

def build_failure_links(goto: list[dict], output: list[list[str]]) -> list[int]:
    """
    Membangun 'failure links' untuk setiap state di Trie.
    Failure link menunjuk ke state lain yang mewakili suffix terpanjang
    dari state saat ini yang juga merupakan prefix dari pola lain.

    Returns:
        list[int]: Array failure, di mana failure[state] adalah state tujuan.
    """
    failure = [0] * len(goto)
    queue = deque()

    # Inisialisasi failure links untuk semua state di level 1
    for char in goto[0]:
        state = goto[0][char]
        if state != 0:
            queue.append(state)

    # Proses sisa state menggunakan Breadth-First Search (BFS)
    while queue:
        state = queue.popleft()
        for char, next_state in goto[state].items():
            queue.append(next_state)
            
            # Tentukan failure link untuk next_state
            f = failure[state]
            while char not in goto[f] and f != 0:
                f = failure[f]
            
            failure[next_state] = goto[f].get(char, 0)

            # Gabungkan output dari failure link ke state saat ini
            # Ini penting untuk menemukan pola yang merupakan suffix dari pola lain
            # (misalnya, menemukan "he" saat kita menemukan "she")
            output[next_state].extend(output[failure[next_state]])

    return failure

def aho_corasick(text: str, patterns: list[str]) -> dict[str, list[int]]:
    """
    Algoritma Aho-Corasick untuk mencari semua kemunculan dari beberapa pola
    dalam sebuah teks secara efisien.

    Args:
        text (str): Teks untuk dicari.
        patterns (list[str]): Daftar pola (kata kunci) yang ingin dicari.

    Returns:
        dict[str, list[int]]: Sebuah dictionary di mana key adalah pola yang
        ditemukan dan value adalah daftar indeks awal kemunculannya.
    """
    if not patterns or not text:
        return {}
        
    goto, output = build_trie(patterns)
    failure = build_failure_links(goto, output)
    
    matches = {pattern: [] for pattern in patterns}
    state = 0

    for i, char in enumerate(text):
        while char not in goto[state] and state != 0:
            state = failure[state]
        
        state = goto[state].get(char, 0)

        # Jika ada output di state ini, berarti ada pola yang cocok
        if output[state]:
            for pattern in output[state]:
                # Posisi akhir adalah i, posisi awal adalah i - len(pattern) + 1
                start_index = i - len(pattern) + 1
                matches[pattern].append(start_index)
                
    return matches


if __name__ == "__main__":
    text = "ushershers"
    patterns = ["he", "she", "his", "hers"]
    
    result = aho_corasick(text, patterns)
    print(f"Mencari pola {patterns} dalam teks '{text}':")
    for pattern, indices in result.items():
        if indices:
            print(f"- Pola '{pattern}' ditemukan di indeks: {indices}")

    print("\n" + "="*20 + "\n")

    text2 = "ANPANMAN"
    patterns2 = "AN"
    result2 = aho_corasick(text2, patterns2)
    print(f"Mencari pola {patterns2} dalam teks '{text2}':")
    for pattern, indices in result2.items():
        if indices:
            print(f"- Pola '{pattern}' ditemukan di indeks: {indices}")