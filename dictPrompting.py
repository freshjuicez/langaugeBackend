from lxml import etree
import os

print(os.getcwd())
# Load and parse the JMdict file
file_path = "c:/Users/howsp/langaugeBackend/langaugeBackend/JMDict_e"  # Path to the extracted file
parser = etree.XMLParser(encoding="utf-8", recover=True)
tree = etree.parse(file_path, parser=parser)
root = tree.getroot()

def find_definitions(word):
    """Find definitions for a given Japanese word."""
    results = []
    for entry in root.findall("entry"):
        # Extract the Japanese words (keb: kanji, reb: reading)
        kanji_elements = entry.findall("k_ele/keb")
        reading_elements = entry.findall("r_ele/reb")
        meanings = entry.findall("sense/gloss")

        kanji_words = [k.text for k in kanji_elements]
        readings = [r.text for r in reading_elements]
        glosses = [g.text for g in meanings]

        # Match the word in kanji or reading
        if word in kanji_words or word in readings:
            results.append({
                "kanji": kanji_words,
                "reading": readings,
                "meanings": glosses
            })

    return results

# Example: Searching for the word "日本"
word_to_search = "日本"
definitions = find_definitions(word_to_search)

# Print results
for result in definitions:
    print("Kanji:", ", ".join(result["kanji"]))
    print("Reading:", ", ".join(result["reading"]))
    print("Meanings:", ", ".join(result["meanings"]))
    print("-" * 40)