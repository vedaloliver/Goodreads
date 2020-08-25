from bs4 import BeautifulSoup
import requests
import sqlite3
import re

#### an issue is that it seems to be looping and only adding data to one cell
### not all of them, and comes up with the last entry

author_l = []
# with open('C:\\Users\\Oliver\\desktop\\code_files\\coursera\\Capstone\\02_Exploring_Data\\Goodreads\\Goodreads_read_100.html', 'r', encoding="utf8") as website:
#     filez = website.read()
#     soup = BeautifulSoup(filez, 'lxml')

#seems to work pretty flawlessly without hitches
### remember though you need to cycle through the pages
count = 0
page = range(1, 5)
for i in page:
    #stuck at getting this done before it went over capactiy
    url = requests.get('https://www.goodreads.com/review/list/25345239-oliver?order=d&page='+ str(i)+'&per_page=30&shelf=read&sort=date_added&utf8=%E2%9C%93&view=table')
    soup = BeautifulSoup(url.text, 'lxml')
    for book in soup.find_all('tr', class_='bookalike review'):
        title = book.find('td', class_='field title').div.a.text.lstrip().rstrip().strip('\n')
        author = book.find('td', class_= 'field author').div.a.text.lstrip().rstrip().strip('\n')
        isbn = book.find('td', class_= 'field isbn').div.text.lstrip().rstrip()
        page_no = book.find('td', class_= 'field num_pages').div.nobr.text.lstrip().rstrip().replace('pp','').replace(' ','').strip('\n')
        date_added = book.find('td', class_= 'field date_added').div.span.text.lstrip().rstrip().strip('\n')
        date_read = book.find('td', class_= 'field date_read').div.div.text.lstrip().rstrip().strip('\n')
        #add this to the main file
        date_published = re.findall(r".*([1-3][0-9]{3})", book.find('td', class_= 'field date_pub').div.text.lstrip().rstrip().strip('\n'))
        date_published1 = ''.join(date_published)
        avg_rating = book.find('td', class_= 'field avg_rating').div.text.lstrip().rstrip().replace(' ','').strip('\n')
        link = book.find('td', class_='field title').div.a.get('href')
        count += 1


            #print(title,author,isbn,page_no,date_added,date_read,avg_rating,link)
        # push scraped data to sql

    
        print(title, date_published1, count)
    ## this is for the review - its out of 5 stars but is a boolean for each star.
    ##figure out how to get and make an average
    #for i in soup.find('tr', class_='bookalike review'):
        #print (book.find('td', class_='field rating').div.div.a.text)


