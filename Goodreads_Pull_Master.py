from bs4 import BeautifulSoup
import sqlite3
import statistics
import grequests
import requests
import re
import progressbar
import time
import genanki

lens = 0
page_no_total = 0
page_no_list = []
list_year = []
year_freq = {}
# for quotes
goodreads_base = 'https://www.goodreads.com'
links = []
complete_quotes = []


# sql initalise
conn = sqlite3.connect('data_init.sqlite')
cur = conn.cursor()
# obtains the tables for statistical analysis
data = cur.execute('''select title.name, title.length, Date_Added.Date  
from title join Date_Added on title.date_added_id=date_added.id 
ORDER BY Date_Added.Date DESC, title.length , title.name  ''')




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
        lens += 1

    for item in list_year:
        if item in year_freq:
            year_freq[item] += 1
        else:
            year_freq[item] = 1

    print('You have read', lens, 'books, which totals', page_no_total, 'pages.\n')
    print('Below is a list of your reading over the years: \n')

    for i in sorted(year_freq, key=year_freq.get, reverse=True):
        print(i, ": ", year_freq[i])

    def mean(books, page_number):
        avg = round(page_number/books, 1)
        print('\n Given the data, on average each book will be',
              avg, 'pages long.\n')

        # add mean for each year

    def std_deviation(page_number):
        std_dev = round(statistics.stdev(page_number), 2)
        print('The standard deviation of the sample is: ', std_dev)

    return(mean(lens, page_no_total), std_deviation(page_no_list))


def author_stats(data):
    print('ketchbutt')
    # apppend authors to a list and count in a dict instances of them appearing
    # it will show a bar graph of your most popular authors
    # for each author add their page count to said dictionary/tuple and return a list of author ranking by page averages

def published_year_stats():


    ## you need to change a parameter if no year is provided to something along the lines of 'no year set'
    ## a weird error pulls if you include both functions at the same time
    

    data_year = cur.execute('''select title.name, title.length, Date_published.year, Author.name
                            from title 
                            join Date_published on title.date_published_id=Date_Published.id
                            join Author on Title.author_id=Author.id
                            ORDER BY Date_Published.Year DESC, title.length ,Author.name, title.name; ''')

    def century():
        list_published_year_freq = []
        published_year_freq = {}
        for i in data_year:
            list_published_year_freq.append((i[2][0:2]))

        for item in list_published_year_freq:
            if item in published_year_freq:
                published_year_freq[item] += 1
            else:
                published_year_freq[item] = 1
        
        print ('Here are the publication dates of the books you have read, sorted by century')
        for i in sorted(published_year_freq, key=published_year_freq.get, reverse=True):
            print(i, ": ", published_year_freq[i])

    def oldest():
        year = []
        for i in data_year:
            if i[2] != str(''):
                year.append((i[0],i[3],i[2]))
        
        author_reversed_new = (' '.join(reversed(year[0][1].split(','))))
        author_reversed_old = (' '.join(reversed(year[-1][1].split(','))))

        print ('\n The newest book you have read is "', year[0][0], '", Written by', author_reversed_new, 'in the year', year[0][2],'.\n')
        print ('\n While the oldest book is "', year[-1][0], '", Written by', author_reversed_old, 'in the year', year[-1][2],'.\n ')
    


    # ok so for some weird reason if you include both of these things it pulls up an error .
    ## im really confused as to why this is the case
    ### you can choose to hide this with a boolean to decide what to show but that's kinda lazy 
    century()
    #oldest()


        
def quote_puller(data2):
    # gathers data from sql
    data2 = cur.execute('''select * FROM quote_link ''')
    # make a list of the Links
    for i in data2:
        links.append(goodreads_base+i[1])

    quote_files = open(r"quotes.txt", "w", encoding='utf-8')
    count = 0
    print("\n Generating quotes, please Wait...\n ")

    def writer():
        global complete_quotes
        prog_count = 0
        for i in range(len(links)):
            lastnumber = range(len(links))[-1]
            progress = (str(round(((i+1)/lastnumber)*100, 1)))
            site = requests.get(links[i])
            soup = BeautifulSoup(site.text, 'lxml')
            count = 0
            # simple progress percentage return
            prog_count += 1
            # nifty boolean which makes it provide percentage completion every 3 ticks and not one.
            if prog_count == 3:
                print("Currently at %", progress, "completion.")
                prog_count = 0
            # gathers the needed quotes
            for quotez in soup.find_all('div', class_='quote'):
                quote = quotez.find('div', class_='quoteText').text
                count += 1
                if count == 5:
                    break
                # next two lines 1. formats for readability and writes to file
                quote_format = quote.replace('\n', '').replace(
                    '”    ―', '”    <br><br><br>    -')+'\n\n'
                complete_quotes.append(quote_format)
    # Takes the scraped quotes and converts them to a format to upload flashcard application anki
    def anki():
        global complete_quotes
        my_model = genanki.Model(
            1607392319,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '<div style="font-family: Helvetica;font-size:35px; padding: 10px; text-align: center;"></div>{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                }, ])

        my_deck = genanki.Deck(
            2059400110,
            'Goodreads Quotes Iona')

        for i in complete_quotes:
            my_note = genanki.Note(
                model=my_model,
                fields=[str(i), ' '])
            my_deck.add_note(my_note)

        genanki.Package(my_deck).write_to_file('Goodreads.apkg')
        print('\n Conversion finished. You will find Goodreads.apkg in this directory. \n')

    writer()
    anki()


def choice():
    print('Do you want to see your reading statistics, or do you want to extract the most popular quotes from each book?')
    while True:
        print('\nStatistics = 1\n\nQuotes = 2:')
        choice = ((input()))
        if choice == str(1):
            print ('What kind of statistics would you like to view?:')
            while True:
                print('\nPage = 1\nAuthor = 2:\nPublication Year = 3\n')
                stat_choice = (input())
                if stat_choice == str(1):
                    page_stats(data)
                    break
                elif stat_choice == str(2):
                    author_stats(data)
                    break
                elif stat_choice == str(3):
                    published_year_stats(data)
                    break
                else:
                    print ("Invalid. Please try again.")
            break     
        elif choice == str(2):
            quote_puller(data)
            break
        else:
            print ("Invalid. Please try again.")

#choice()
published_year_stats()
