import sqlite3

def find_definitions_db(word, db_path="jmdict.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT kanji, reading, meanings FROM entries
    WHERE kanji = ? OR reading = ?
    """, (word, word))
    results = cursor.fetchall()

    conn.close()
    return [{"kanji": r[0], "reading": r[1], "meanings": r[2]} for r in results]

# Example query
definitions = find_definitions_db("嘘")
for result in definitions:
    print("Kanji:", result["kanji"])
    print("Reading:", result["reading"])
    print("Meanings:", result["meanings"])
    print("-" * 40)
