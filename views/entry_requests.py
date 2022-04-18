import json
import sqlite3

from models.entry import Entry
from models.mood import Mood


def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
    SELECT
      e.concept,
      e.entry,
      e.mood_id,
      e.date,
      e.id,
      m.label mood_label
    FROM Entry e
    JOIN Mood m
      ON m.id = e.mood_id
    """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entry(row['concept'],
                          row['entry'],
                          row['mood_id'],
                          row['date'],
                          row['id']
                          )
            mood = Mood(row['mood_id'],
                        row['mood_label']
                        )

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)
    return json.dumps(entries)
