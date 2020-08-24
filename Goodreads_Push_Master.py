from bs4 import BeautifulSoup
import grequests
import requests
import urllib
import sqlite3
import datetime
import re

# sql initialise
conn = sqlite3.connect('data_init.sqlite')
cur = conn.cursor()

# generate tables
cur.executescript('''
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Title;
DROP TABLE IF EXISTS Date_Added;
DROP TABLE IF EXISTS Quote_Link;

CREATE TABLE Author (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);
CREATE TABLE Title (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT  UNIQUE,
    author_id  INTEGER,
    date_added_id INTEGER,
    quote_link_id INTEGER,
    length INTEGER, avg_rating INTEGER,link TEXT UNIQUE, isbn INTEGER
);
CREATE TABLE Date_Added (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Date   TEXT UNIQUE
);

CREATE TABLE quote_link (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    quote_link   TEXT UNIQUE
);
''')

# site open and detail scrape
with open('C:\\Users\\Oliver\\desktop\\code_files\\coursera\\Capstone\\02_Exploring_Data\\Goodreads\\Goodreads_read_100.html', 'r', encoding="utf8") as website:
    filez = website.read()
    soup = BeautifulSoup(filez, 'lxml')

links = []

def quote_extract(links):
    #initalise grequests to use 
    reqs = (grequests.get(link) for link in links)
    resp = grequests.imap(reqs, grequests.Pool(1))
    #opens up grequests and finds tags within each consecutive webpage for the quote hyperlink
    # pulls the quote hyperlink to produce
    for i in resp:
        soups = BeautifulSoup(i.text, 'lxml')
        for j in  soups.find_all('a',class_='actionLink', attrs={'href': re.compile("^/work/quotes")}):
            quotes = (j.get('href'))
            print(quotes)

            #independent push to sql as it wasnt working with everything else
            cur.execute('''INSERT or REPLACE INTO Quote_link (quote_link)
                VALUES ( ? )''', (quotes, ))
            cur.execute('SELECT id FROM Quote_link WHERE quote_link = ?', (quotes, ))
            quote_link_id = cur.fetchone()[0]

            conn.commit()


#master scraping element - neeeds to be put into a function
# pulls all the needed data 
for book in soup.find_all('tr', class_='bookalike review'):
    name = book.find('td', class_='field title').div.a.text.lstrip().rstrip().strip('\n')
    author = book.find('td', class_='field author').div.a.text.lstrip().rstrip().strip('\n')
    page_no = book.find('td', class_='field num_pages').div.nobr.text.lstrip().rstrip().replace('pp', '').replace(' ', '').replace(',', '').strip('\n')
    date_added = book.find('td', class_='field date_added').div.span.text.lstrip().rstrip().strip('\n')
    date_added_f = datetime.datetime.strptime(date_added, '%b %d, %Y').date()
    date_read = book.find('td', class_='field date_read').div.div.text.replace('[edit]', '').lstrip().rstrip().strip('\n')
    avg_rating = book.find('td', class_='field avg_rating').div.text.lstrip().rstrip().replace(' ', '').strip('\n')
    link = book.find('td', class_='field title').div.a.get('href')
    links.append(book.find('td', class_='field title').div.a.get('href'))
    quotes = 'null'
    # for consistency's sake if no isbn is present, a message is produced 
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
        (name, author_id,date_added_id,quote_link_id, length, avg_rating, link, isbn) 
        VALUES ( ?, ?,? , ?, ?, ?, ?, ?)''',
                (name, author_id, date_added_id,quote_link_id, page_no, avg_rating, link, isbn))

    conn.commit()


quote_extract(links)