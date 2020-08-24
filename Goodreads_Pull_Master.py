from bs4 import BeautifulSoup
import sqlite3
import statistics
import grequests
import requests
import re
import progressbar
import time

#sql initalise
conn = sqlite3.connect('data_init_1080backup.sqlite')
cur = conn.cursor()
#obtains the tables for statistical analysis
data = cur.execute('''select title.name, title.length, Date_Added.Date  
from title join Date_Added on title.date_added_id=date_added.id 
ORDER BY Date_Added.Date DESC, title.length , title.name  ''')

lens = 0
page_no_total = 0
page_no_list = []
list_year = []
year_freq = {}
def page_stats(datas):
    global lens
    global page_no_total
    global year_freq
    global page_no_list
    for i in data:
        #print (i[0],',', i[1],',',i[2])
        list_year.append((i[2].split('-'))[0])
        page_no_total += int(i[1])
        page_no_list.append(int(i[1]))
        lens +=1

    for item in list_year:
        if item in year_freq:
            year_freq[item] +=1
        else:
            year_freq[item] = 1

    print ('You have read', lens, 'books, which totals', page_no_total, 'pages.\n')
    print ('Below is a list of your reading over the years: \n')
    
    for i in sorted(year_freq, key=year_freq.get, reverse=True):
                print(i, ": ", year_freq[i])

    
    def mean(books, page_number):
        avg = round(page_number/books, 1)
        print ('\n Given the data, on average each book will be', avg, 'pages long.\n')

        # add mean for each year

    def std_deviation(page_number):
        std_dev = round(statistics.stdev(page_number),2)
        print ('The standard deviation of the sample is: ', std_dev)

    return(mean(lens,page_no_total), std_deviation(page_no_list))

def author_stats(data):
    pass
    # apppend authors to a list and count in a dict instances of them appearing
    # it will show a bar graph of your most popular authors
    #for each author add their page count to said dictionary/tuple and return a list of author ranking by page averages

#pulls the table data for quote scraping 
goodreads_base = 'https://www.goodreads.com'
links = []
count = 0
prog_count = 0
def quote_puller(data2):
    global count
    global prog_count
    data2 = cur.execute('''select * FROM quote_link ''')
    for i in data2:
        links.append(goodreads_base+i[1])

    site = requests.get(links[43])
    soup = BeautifulSoup(site.text, 'lxml')
    quote_files = open(r"quotes.txt", "w", encoding='utf-8')

    print ("Please Wait...")
    
    for i in range(len(links)):
        lastnumber = range(len(links))[-1]
        progress = (str(round(((i+1)/lastnumber)*100, 1)))
        #print (lastnumber)
        site = requests.get(links[i])
        soup = BeautifulSoup(site.text, 'lxml')
        count = 0
        prog_count +=1
        if prog_count == 2:
            print ("Currently at %", progress, "completion.")
            prog_count=0
        for quotez in soup.find_all('div', class_='quote'):
            quote = quotez.find('div', class_='quoteText').text
            count += 1
            if count == 5:
                break
    
            quote_format = str(count)+ ': ' +quote.replace('\n', '').replace('”    ―','”    \n \n')+'\n\n'
            quote_files.write(str(quote_format))

            #print ("quote:",count ,  quote.replace('\n', ''), '\n')
    

    # for i in resp:
    #     soups = BeautifulSoup(i.text, 'lxml')
    #     for quotez in soups.find_all('div', class_='quote'):
    #         quote = quotez.find('div', class_='quoteText').text
    #         count += 1
    #         if count == 5:
    #             break

    #         quote_format = str(count)+ ': ' +quote.replace('\n', '').replace('”    ―','”    \n \n')+'\n\n'
    #         quote_files.write(str(quote_format))

    #         print ("quote:",count ,  quote.replace('\n', ''), '\n')
        
#page_stats(data)
quote_puller(data)

