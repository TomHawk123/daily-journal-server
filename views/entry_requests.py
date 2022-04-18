import json
import sqlite3

from models.entry import Entry
from models.mood import Mood


def get_all_entries():
    with sqlite3.connect("./journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
    SELECT
        e.id,
        e.concept,
        e.entry,
        e.mood_id,
        e.date,
        m.label mood_label
    FROM Entry e
    JOIN Mood m
        ON m.id = e.mood_id
    """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entry(
                row['id'],
                row['concept'],
                row['entry'],
                row['mood_id'],
                row['date']
            )
            mood = Mood(
                row['mood_id'],
                row['mood_label']
            )

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)
    return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM entry e
        JOIN Mood m
            ON m.id = e.mood_id
        WHERE e.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        mood = Mood(
            data['mood_id'],
            data['mood_label']
        )

        # Create an Entry instance from the current row
        entry = Entry(
            data['id'],
            data['concept'],
            data['entry'],
            data['mood_id'],
            data['date']
        )

        entry.mood = mood.__dict__
        return json.dumps(entry.__dict__)


def delete_entry(id):
    with sqlite3.connect("./journal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))


def get_entry_by_search(entry):
    with sqlite3.connect("./journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM Entry e
        JOIN Mood m
            ON e.mood_id = m.id
        WHERE e.entry LIKE ?
        """, (f"%{entry}%", ))
        # have to use question marks in query, in the tuple part input the thing you want

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(
                row['id'],
                row['concept'],
                row['entry'],
                row['mood_id'],
                row['date']
            )

            mood = Mood(
                row['id'],
                row['mood_label']
            )
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_entry(new_entry):
    with sqlite3.connect("./journal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
        (concept, entry, mood_id, date)
        VALUES
            (?, ?, ?, ?);
        """, (
            new_entry['concept'],
            new_entry['entry'],
            new_entry['mood_id'],
            new_entry['date']
        )
        )

        id = db_cursor.lastrowid
        new_entry['id'] = id

    return json.dumps(new_entry)
