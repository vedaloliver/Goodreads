from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

# sql initialise
conn = sqlite3.connect('data_init.sqlite')
cur = conn.cursor()
# generate tables

cur.executescript('''
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Title;
DROP TABLE IF EXISTS Date_Added;

CREATE TABLE Author (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);
CREATE TABLE Title (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT  UNIQUE,
    author_id  INTEGER,
    date_added_id INTEGER,
    length INTEGER, avg_rating INTEGER,link TEXT UNIQUE, isbn INTEGER
);
CREATE TABLE Date_Added (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Date   TEXT UNIQUE
);
''')

# site open and detail scrape
with open('C:\\Users\\Oliver\\desktop\\code_files\\coursera\\Capstone\\02_Exploring_Data\\Goodreads\\Goodreads_read_100.html', 'r', encoding="utf8") as website:
    filez = website.read()
    soup = BeautifulSoup(filez, 'lxml')

#isbn = ''
for book in soup.find_all('tr', class_='bookalike review'):
    name = book.find('td', class_='field title').div.a.text.lstrip().rstrip().strip('\n')
    author = book.find('td', class_='field author').div.a.text.lstrip().rstrip().strip('\n')
    page_no = book.find('td', class_='field num_pages').div.nobr.text.lstrip().rstrip().replace('pp', '').replace(' ', '').replace(',', '').strip('\n')
    date_added = book.find('td', class_='field date_added').div.span.text.lstrip().rstrip().strip('\n')
    date_added_f = datetime.datetime.strptime(date_added, '%b %d, %Y').date()
    date_read = book.find('td', class_='field date_read').div.div.text.replace('[edit]', '').lstrip().rstrip().strip('\n')
    avg_rating = book.find('td', class_='field avg_rating').div.text.lstrip().rstrip().replace(' ', '').strip('\n')
    link = book.find('td', class_='field title').div.a.get('href')
    if len(book.find('td', class_='field isbn').div.text.lstrip().rstrip()) in range(6, 13):
        isbn = book.find('td', class_='field isbn').div.text.lstrip().rstrip()
    else:
        isbn = 'NULL'

    # push scraped data to sql
    cur.execute('''INSERT or IGNORE INTO Author (name)
        VALUES( ? )''', (author, ))
    cur.execute('SELECT id FROM Author WHERE name = ? ', (author, ))
    author_id = cur.fetchone()[0]

    cur.execute('''INSERT or IGNORE INTO Date_Added (Date)
        VALUES ( ? )''', (date_added_f, ))
    cur.execute('SELECT id FROM Date_added WHERE Date = ?', (date_added_f, ))
    date_added_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Title
        (name, author_id,date_added_id, length, avg_rating, link, isbn) 
        VALUES ( ?, ?,? , ?, ?, ?, ?)''',
                (name, author_id, date_added_id, page_no, avg_rating, link, isbn))

    conn.commit()
