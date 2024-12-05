import sqlite3
from lxml import etree
import os

print("Current Working Directory:", os.getcwd())

# Load and parse the JMdict file
file_path = "JMDict_e"
parser = etree.XMLParser(encoding="utf-8", recover=True)
tree = etree.parse(file_path, parser=parser)
root = tree.getroot()

def create_database(db_path="jmdict.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table for entries
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kanji TEXT,
        reading TEXT,
        meanings TEXT
    )
    """)

    # Insert data
    for entry in root.findall("entry"):
        # Extract kanji, readings, and meanings
        kanji_elements = entry.findall("k_ele/keb")
        reading_elements = entry.findall("r_ele/reb")
        meanings = entry.findall("sense/gloss")

        # Handle cases where kanji or reading might be missing
        kanji_words = [k.text for k in kanji_elements] or [None]
        readings = [r.text for r in reading_elements] or [None]
        glosses = "; ".join([g.text for g in meanings]) or None

        # Insert separate rows for each kanji-reading combination
        for kanji in kanji_words:
            for reading in readings:
                cursor.execute(
                    "INSERT INTO entries (kanji, reading, meanings) VALUES (?, ?, ?)",
                    (kanji, reading, glosses)
                )

    conn.commit()
    conn.close()

create_database()
