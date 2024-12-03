import sqlite3
from lxml import etree
import os

print(os.getcwd())
# Load and parse the JMdict file
file_path = "c:/Users/howsp/langaugeBackend/langaugeBackend/JMDict_e"  # Path to the extracted file
parser = etree.XMLParser(encoding="utf-8", recover=True)
tree = etree.parse(file_path, parser=parser)
root = tree.getroot()

def create_database(db_path="jmdict.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        kanji TEXT,
        reading TEXT,
        meanings TEXT
    )
    """)

    # Insert data
    for entry in root.findall("entry"):
        kanji_elements = entry.findall("k_ele/keb")
        reading_elements = entry.findall("r_ele/reb")
        meanings = entry.findall("sense/gloss")

        kanji_words = ", ".join([k.text for k in kanji_elements])
        readings = ", ".join([r.text for r in reading_elements])
        glosses = "; ".join([g.text for g in meanings])

        cursor.execute("INSERT INTO entries (kanji, reading, meanings) VALUES (?, ?, ?)",
                       (kanji_words, readings, glosses))

    conn.commit()
    conn.close()

create_database()
