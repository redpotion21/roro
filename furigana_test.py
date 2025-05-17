from fugashi import Tagger

def kata_to_hira(katakana):
    # Convert Katakana to Hiragana
    return ''.join(
        chr(ord(char) - 0x60) if 'ァ' <= char <= 'ン' else char
        for char in katakana
    )

def contains_kanji(text):
    # Check if any character is Kanji
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)

tagger = Tagger()
text = "日本語の勉強をしています。"

result = []

for word in tagger(text):
    surface = word.surface
    try:
        reading = word.feature.pron or word.feature.kana or surface
        reading_hira = kata_to_hira(reading)
    except AttributeError:
        reading_hira = surface

    if contains_kanji(surface):
        result.append(f"{surface}({reading_hira})")  # Format: Kanji(Furigana)
    else:
        result.append(surface)

# Output
output = ''.join(result)
print(output)
