import json
import sqlite3
import sys

print('''
    ------------------------
    Enter json file path which meets specified requirements
    If file name is not specified then default file 'roaster_data.json' is selected
    ------------------------
''')

# Reading json data from file
fname = input("File Path: ")
if len(fname) < 1:
    fname = "roster_data.json"

try:
    fh = open(fname)
    print(fname, "file found")
except:
    print('unable to open specified file')
    sys.exit()

try:
    str_data = fh.read()
    print('Successfully read file')
except:
    print("unable to read data from given file")
    sys.exit()

try:
    json_data = json.loads(str_data)
    print("parsed json data")
except:
    print('unable to parse json data from file')
    sys.exit()


# Creating a sqlite database with required tables
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

count = 0
for entry in json_data:
    if len(entry) != 3:
        continue
    name = entry[0]
    title = entry[1]
    role = entry[2]

    print(name, title, role)
    
    cur.execute('INSERT OR IGNORE INTO user (name) VALUES (?)', (name, ))
    cur.execute('SELECT id FROM user WHERE name = ?', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (title, ))
    cur.execute('SELECT id FROM Course WHERE title = ?', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)', (user_id, course_id, role))
    
    count += 1
    if count % 100 == 0:
        conn.commit()