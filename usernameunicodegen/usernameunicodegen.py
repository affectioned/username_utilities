import itertools

unicode_map = {
    "a": "а",  # Cyrillic 'a'
    "c": "с",  # Cyrillic 's'
    "e": "е",  # Cyrillic 'e'
    "i": "і",  # Cyrillic 'i'
    "j": "ј",  # Cyrillic 'j'
    "o": "ο",  # Greek small omicron
    "p": "р",  # Cyrillic 'r' (looks like p)
    "s": "ѕ",  # Cyrillic 's'
    "x": "х",  # Cyrillic 'h' looks like x
    "y": "у",  # Cyrillic 'u' looks like y

    "A": "Α",  # Greek capital Alpha
    "B": "Β",  # Greek capital Beta
    "C": "С",  # Cyrillic capital Es
    "E": "Ε",  # Greek capital Epsilon
    "H": "Η",  # Greek capital Eta
    "I": "Ι",  # Greek capital Iota
    "J": "Ј",  # Cyrillic capital Je
    "K": "Κ",  # Greek capital Kappa
    "M": "Μ",  # Greek capital Mu
    "N": "Ν",  # Greek capital Nu
    "O": "Ο",  # Greek capital Omicron
    "P": "Ρ",  # Greek capital Rho
    "S": "Ѕ",  # Cyrillic capital Dze (looks like Latin S)
    "T": "Τ",  # Greek capital Tau
    "X": "Χ",  # Greek capital Chi
    "Y": "Υ",  # Greek capital Upsilon
    "Z": "Ζ"   # Greek capital Zeta
}

def generate_variations_in_stages(word, unicode_map):
    # Identify all positions in the word that can be replaced
    replaceable_positions = [(i, unicode_map[char]) for i, char in enumerate(word) if char in unicode_map]

    # We'll build a list of lists, where each sublist corresponds to variations
    # with a certain number of replaced characters.
    all_stages = []
    for r in range(1, len(replaceable_positions) + 1):
        stage_variations = []
        for combo in itertools.combinations(replaceable_positions, r):
            new_word = list(word)
            for pos, replacement in combo:
                new_word[pos] = replacement
            stage_variations.append("".join(new_word))
        all_stages.append(stage_variations)
    return all_stages

def main():
    word = input("Enter a word: ").strip()
    stages = generate_variations_in_stages(word, unicode_map)

    if not any(stages):
        print("No variations for this word found")
    else:
        variation_index = 1
        for r, stage_variations in enumerate(stages, start=1):
            if stage_variations:
                print(f"\nVariations with {r} character(s) replaced:")
                for variation in stage_variations:
                    print(f"[{variation_index}] {variation}")
                    variation_index += 1

if __name__ == "__main__":
    main()