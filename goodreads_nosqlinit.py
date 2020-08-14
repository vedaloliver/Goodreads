from bs4 import BeautifulSoup
import requests
import sqlite3

#### an issue is that it seems to be looping and only adding data to one cell
### not all of them, and comes up with the last entry

#sql
##sql initialise
author_l = []
# site open and detail scrape
   #url = requests.get('https://www.goodreads.com/review/list/25345239-oliver?utf8=%E2%9C%93&order=d&shelf=read&sort=date_added&utf8=%E2%9C%93&view=table&title=oliver&per_page=100')
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
    # push scraped data to sql

   
print(author)
    ## this is for the review - its out of 5 stars but is a boolean for each star.
    ##figure out how to get and make an average
    #for i in soup.find('tr', class_='bookalike review'):
        #print (book.find('td', class_='field rating').div.div.a.text)


