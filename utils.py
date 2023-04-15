import re


def remove_ruby_tags(text):
    return re.sub(r"<ruby>(.*?)<rt>.*?</rt></ruby>", r"\1", text)


def split_sentence(text):
    sentences = re.findall(r"[^。！？\!\?]+[。！？\!\?]", text)
    if len(sentences) == 0:
        return [text]
    return sentences


hiragana_range = (0x3041, 0x3096)
katakana_range = (0x30A1, 0x30F6)

translation_table = str.maketrans(
    {
        chr(code): chr(code - hiragana_range[0] + katakana_range[0])
        for code in range(hiragana_range[0], hiragana_range[1] + 1)
    }
)


def to_katakana(text):
    return text.translate(translation_table)
