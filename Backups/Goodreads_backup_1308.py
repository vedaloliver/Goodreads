from bs4 import BeautifulSoup
import requests
import sqlite3

#### an issue is that it seems to be looping and only adding data to one cell
### not all of them, and comes up with the last entry

#sql
##sql initialise
conn = sqlite3.connect('data_init.sqlite')
cur = conn.cursor()
## generate tables
cur.executescript('''
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Title;

CREATE TABLE Author (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE

);

CREATE TABLE Title (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    author_id  INTEGER,
    length INTEGER, avg_rating INTEGER,link TEXT UNIQUE,date_read TEXT UNIQUE, isbn INTEGER
);
''')


# site open and detail scrape
with open('C:\\Users\\Oliver\\desktop\\code_files\\coursera\\Capstone\\02_Exploring_Data\\Goodreads\\Goodreads_read_100.html', 'r', encoding="utf8") as website:
    filez = website.read()
    soup = BeautifulSoup(filez, 'lxml')

for book in soup.find_all('tr', class_='bookalike review'):
    title = book.find('td', class_='field title').div.a.text.lstrip().rstrip().strip('\n')
    author = book.find('td', class_= 'field author').div.a.text.lstrip().rstrip().strip('\n')
    isbn = book.find('td', class_= 'field isbn').div.text.lstrip().rstrip()
    page_no = book.find('td', class_= 'field num_pages').div.nobr.text.lstrip().rstrip().replace('pp','').replace(' ','').strip('\n')
    date_added = book.find('td', class_= 'field date_added').div.span.text.lstrip().rstrip().strip('\n')
    date_read = book.find('td', class_= 'field date_read').div.div.text.lstrip().rstrip().strip('\n')
    avg_rating = book.find('td', class_= 'field avg_rating').div.text.lstrip().rstrip().replace(' ','').strip('\n')
    link = book.find('td', class_='field title').div.a.get('href')

    #print(title,author,isbn,page_no,date_added,date_read,avg_rating,link)
    #print (author)
# push scraped data to sql

    cur.execute('''INSERT or IGNORE INTO Author (name)
        VALUES( ? )''', (author, )  )
    cur.execute('SELECT id FROM Author WHERE name = ? ',(author, ))
    author_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Title
        (title, author_id, length, avg_rating, link, isbn) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', 
        ( title, author_id, page_no, avg_rating, link , isbn) )

    conn.commit()

print(len(author))
    ## this is for the review - its out of 5 stars but is a boolean for each star.
    ##figure out how to get and make an average
    #for i in soup.find('tr', class_='bookalike review'):
        #print (book.find('td', class_='field rating').div.div.a.text)


