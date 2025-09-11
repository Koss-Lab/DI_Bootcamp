#ExercisesXP.py

import os
import urllib.request
import zipfile
from functools import partial

import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
from sqlalchemy import inspect


# Dataset: download if needed
def ensure_chinook_db():
    chinook_url = 'http://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip'
    if not os.path.exists('chinook.db'):
        if not os.path.exists('chinook.zip'):
            print('downloading chinook.zip ', end='')
            with urllib.request.urlopen(chinook_url) as response:
                with open('chinook.zip', 'wb') as f:
                    for data in iter(partial(response.read, 4 * 1024), b''):
                        print('.', end='', flush=True)
                        f.write(data)
            print()
        zipfile.ZipFile('chinook.zip').extractall()
    assert os.path.exists('chinook.db'), "chinook.db is missing. Place it next to this script."


# Call the dataset setup
ensure_chinook_db()


# Helpers (console-friendly version of the prompt’s helpers)
def sql(query):
    print("\n", query, "\n")


def get_results(query, engine):
    # Accept ORM Query or raw SQL string
    try:
        q = query.statement  # ORM Query
    except AttributeError:
        q = query            # raw SQL text/str
    return pd.read_sql(q, engine)


def display_results(query, engine, head=None):
    df = get_results(query, engine)
    if head is not None:
        print(df.head(head).to_string(index=False))
    else:
        print(df.to_string(index=False))
    sql(query)


# 🌟 Exercise 1: Open the database (engine, cur, reflect, automap, session)
engine = sqlalchemy.create_engine("sqlite:///chinook.db")  # engine variable name per prompt
cur = engine.connect()                                     # cur variable name per prompt

metadata = sqlalchemy.MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

Session = sessionmaker(bind=engine)
session = Session()

print("Exercise 1 ✅ engine, cur, reflection, automap, session ready.")


# 🌟 Exercise 2: table names
print("\n🌟 Exercise 2: table names")
inspector = inspect(engine)
tables = inspector.get_table_names()
print(tables)  # print out all the table names (as required)


# ORM class handles
Track = Base.classes.tracks
Album = Base.classes.albums
Artist = Base.classes.artists
InvoiceItem = Base.classes.invoice_items


# 🌟 Exercise 3: first three tracks
print("\n🌟 Exercise 3: first three tracks")
q3 = session.query(Track).limit(3)
display_results(q3, engine)


# 🌟 Exercise 4: track name + album title (first 20)
print("\n🌟 Exercise 4: track name + album title (first 20)")
q4 = (
    session.query(Track.Name, Album.Title)
    .join(Album, Track.AlbumId == Album.AlbumId)
    .limit(20)
)
display_results(q4, engine)


# 🌟 Exercise 5: first 10 track sales (name + quantity)
print("\n🌟 Exercise 5: first 10 track sales (name + quantity)")
q5 = (
    session.query(Track.Name, InvoiceItem.Quantity)
    .join(InvoiceItem, Track.TrackId == InvoiceItem.TrackId)
    .limit(10)
)
display_results(q5, engine)


# 🌟 Exercise 6: top 10 tracks sold
print("\n🌟 Exercise 6: top 10 tracks sold")
q6 = (
    session.query(Track.Name, func.sum(InvoiceItem.Quantity).label("TotalSold"))
    .join(InvoiceItem, Track.TrackId == InvoiceItem.TrackId)
    .group_by(Track.Name)
    .order_by(func.sum(InvoiceItem.Quantity).desc())
    .limit(10)
)
display_results(q6, engine)


# 🌟 Exercise 7: top 10 highest selling artists
print("\n🌟 Exercise 7: top 10 highest selling artists")
q7 = (
    session.query(Artist.Name, func.sum(InvoiceItem.Quantity).label("TotalSold"))
    .join(Album, Artist.ArtistId == Album.ArtistId)
    .join(Track, Album.AlbumId == Track.AlbumId)
    .join(InvoiceItem, Track.TrackId == InvoiceItem.TrackId)
    .group_by(Artist.Name)
    .order_by(func.sum(InvoiceItem.Quantity).desc())
    .limit(10)
)
display_results(q7, engine)

print("\nAll exercises ✅ Done.")
