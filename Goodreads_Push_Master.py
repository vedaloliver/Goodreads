from bs4 import BeautifulSoup
import grequests
import requests
import urllib
import sqlite3
import datetime
import re

conn = sqlite3.connect('data_init.sqlite')
cur = conn.cursor()

links = []
book_n = 0 

#SQL table initaliser
def SQL_init():
    # generates database objects in SQLite
    cur.executescript('''
    DROP TABLE IF EXISTS Author;
    DROP TABLE IF EXISTS Title;
    DROP TABLE IF EXISTS Date_Added;
    DROP TABLE IF EXISTS Quote_Link;
    DROP TABLE IF EXISTS Date_Published;

    CREATE TABLE Author (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT UNIQUE
    );
    CREATE TABLE Title (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT  UNIQUE,
        author_id  INTEGER,date_added_id INTEGER,quote_link_id INTEGER,
        date_published_id INTEGER,length INTEGER, avg_rating INTEGER,link TEXT UNIQUE, isbn INTEGER
    );
    CREATE TABLE Date_Added (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Date   TEXT UNIQUE
    );

    CREATE TABLE Date_Published (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Year   TEXT UNIQUE
    );

    CREATE TABLE quote_link (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        quote_link   TEXT UNIQUE
    );
    ''')

SQL_init()

print("Please wait...\n")

#master scraping element - pulls all the needed data for analysis
def scrape():
    global book_n
    #user_id = 0

    def SQL_commit():
        # push scraped data to sql
        cur.execute('''INSERT or IGNORE INTO Author (name)
            VALUES( ? )''', (author, ))
        cur.execute('SELECT id FROM Author WHERE name = ? ', (author, ))
        author_id = cur.fetchone()[0]

        cur.execute('''INSERT or IGNORE INTO Date_Added (Date)
            VALUES ( ? )''', (date_added_f, ))
        cur.execute('SELECT id FROM Date_added WHERE Date = ?', (date_added_f, ))
        date_added_id = cur.fetchone()[0]

        cur.execute('''INSERT or IGNORE INTO Date_Published (Year)
            VALUES ( ? )''', (date_published1, ))
        cur.execute('SELECT id FROM Date_Published WHERE Year = ?', (date_published1, ))
        date_published_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO Title
            (name,length, avg_rating, link, isbn, author_id, date_added_id, date_published_id) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name,  page_no, avg_rating, link, isbn, author_id, date_added_id,date_published_id))

        conn.commit()


    print('''Please provide your user ID.\nThis can be found by directing to your user profile and locating the string of numbers in the url at the top of the page.\n ''')

    while True:
        try:
            user_id = int(input('Enter your id:'))
            print ('\nThank you. ')
            break
        except ValueError:
            print ("Invalid id. Try again")
    
    page = range(1, 5)
    for i in page:
        url = requests.get('https://www.goodreads.com/review/list/' +str(user_id) +'?order=d&page='+ str(i)+'&per_page=30&shelf=read&sort=date_added&utf8=%E2%9C%93&view=table')
        soup = BeautifulSoup(url.text, 'lxml')
        for book in soup.find_all('tr', class_='bookalike review'):
            name = book.find('td', class_='field title').div.a.text.lstrip().rstrip().strip('\n')
            author = book.find('td', class_='field author').div.a.text.lstrip().rstrip().strip('\n')
            page_no = book.find('td', class_='field num_pages').div.nobr.text.lstrip().rstrip().replace('pp', '').replace(' ', '').replace(',', '').strip('\n')
            date_added = book.find('td', class_='field date_added').div.span.text.lstrip().rstrip().strip('\n')
            date_added_f = datetime.datetime.strptime(date_added, '%b %d, %Y').date()
            date_read = book.find('td', class_='field date_read').div.div.text.replace('[edit]', '').lstrip().rstrip().strip('\n')
            date_published = re.findall(r".*([1-3][0-9]{3})", book.find('td', class_= 'field date_pub').div.text.lstrip().rstrip().strip('\n'))
            date_published1 = ''.join(date_published)
            avg_rating = book.find('td', class_='field avg_rating').div.text.lstrip().rstrip().replace(' ', '').strip('\n')
            link = book.find('td', class_='field title').div.a.get('href')
            links.append("https://www.goodreads.com/"+ book.find('td', class_='field title').div.a.get('href'))
            quotes = 'null'
            # for consistency's sake if no isbn is present, a message is produced 
            if len(book.find('td', class_='field isbn').div.text.lstrip().rstrip()) in range(6, 13):
                isbn = book.find('td', class_='field isbn').div.text.lstrip().rstrip()
            else:
                isbn = 'NULL'
            book_n += 1 
            
            #print (book_n)
            
            SQL_commit()
    
    print('\n ...\n')

#Separate function for withdrawing the book's quote links
def quote_extract():
    prog_count = 0
    ticker = 0
    #initalise grequests to use 
    reqs = (grequests.get(link) for link in links)
    resp = grequests.imap(reqs, grequests.Pool(1))

    def SQL_commit():
        nonlocal quotes
        cur.execute('''INSERT or REPLACE INTO Quote_link (quote_link)
            VALUES ( ? )''', (quotes, ))
        cur.execute('SELECT id FROM Quote_link WHERE quote_link = ?', (quotes, ))
        quote_link_id = cur.fetchone()[0]

        conn.commit()

    for i in resp:
        soups = BeautifulSoup(i.text, 'lxml')
        for j in  soups.find_all('a',class_='actionLink', attrs={'href': re.compile("^/work/quotes")}):
            quotes = (j.get('href'))
            prog_count += 1 
            progress =  (str(round((prog_count/book_n)*100, 1)))
            ticker += 1
            if ticker == 3:
                print("Currently at %", progress, "completion.")
                ticker = 0         
    
            SQL_commit()

scrape()
quote_extract()

print ('\nFinished committing to the database.\n')