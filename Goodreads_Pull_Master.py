from bs4 import BeautifulSoup
import sqlite3
import math
import statistics
import grequests
import requests
import re
import genanki

lens = 0
page_no_total = 0
page_no_list = []
list_year = []
year_freq = {}
# for quotes
goodreads_base = 'https://www.goodreads.com'
links = []
complete_quotes_anki = []
complete_quotes_txt = []


# sql initalise
conn = sqlite3.connect('data_init.sqlite')
cur = conn.cursor()
# obtains the tables for statistical analysis
data = cur.execute('''select Title.name, Title.length, Date_Added.Date  
from Title join Date_Added on title.date_added_id=date_added.id 
ORDER BY Date_Added.Date DESC, title.length , title.name  ''')


def page_stats():
    # Provides simple stats based on averages of pages read in each book
    global lens
    global page_no_total
    global year_freq
    global page_no_list


    for i in data:
        list_year.append((i[2].split('-'))[0])
        page_no_total += int(i[1])
        page_no_list.append(int(i[1]))
        lens += 1

    for item in list_year:
        if item in year_freq:
            year_freq[item] += 1
        else:
            year_freq[item] = 1

    def books_lens_total():
        print('You have read', lens, 'books, which totals', page_no_total, 'pages.\n')
        print('Below is a list of your reading over the years: \n')

        for i in sorted(year_freq, key=year_freq.get, reverse=True):
            print(i, ": ", year_freq[i])

    def mean(books, page_number):
        avg = round(page_number/books, 1)
        print('\nGiven the data, on average each book will be',
              avg, 'pages long.\n')


    def std_deviation(page_number):
        std_dev = round(statistics.stdev(page_number), 2)
        print('The standard deviation of the sample is: ', std_dev)

    ### come back to this as you have to change things around 

    # def biggest_smallest():
    #     # returns the biggest and smallest book read    
    #     author_reversed_new = (' '.join(reversed(year[0][1].split(','))))
    #     author_reversed_old = (' '.join(reversed(year[-1][1].split(','))))

    #     print ('\nThe biggest book you have read is"', max(page_no_list), '", Written by', author_reversed_new, 'in the year', year[0][2],',')
    #     print ('While the smallest book is"', min(page_no_list), '", Written by', author_reversed_old, 'in the year', year[-1][2],'.\n ')
    

    return(books_lens_total(),mean(lens, page_no_total), std_deviation(page_no_list),end_choices() )

    
def author_stats():
    # Simple in this current verison - only produces the authors with the most read books by you
    data_auth = cur.execute('''select Title.name, title.length, Author.name
                            from title 
                            join Author on Title.author_id=Author.id
                            ORDER BY Author.name DESC, title.length, title.name; ''')

    # do author average rating
  
    def top_10():
        count = 0
        list_author_freq = []
        dict_author_freq = {}
        for i in data_auth:
            list_author_freq.append(' '.join(reversed(i[2].split(','))))


        for item in list_author_freq:
            if item in dict_author_freq:
                dict_author_freq[item] += 1
            else:
                dict_author_freq[item] = 1

        print ('\nBelow are the top 10 most read books by each author:\n ')
        count = 0
        for i in sorted(dict_author_freq, key=dict_author_freq.get, reverse=True):
            print(i, ": ", dict_author_freq[i])
            count += 1
            if count == 10:
                break
    top_10()


    #return (end_choices())

def published_year_stats():

    data_year = cur.execute('''select title.name, title.length, Date_published.year,title.avg_rating, Author.name
                            from title 
                            join Date_published on title.date_published_id=Date_Published.id
                            join Author on Title.author_id=Author.id
                            ORDER BY Date_Published.Year DESC, title.length,title.avg_rating,Author.name, title.name; ''')
    year = []
    list_published_year_freq = []

    # loop initiates outside other functions as i learn that a loop cannot be run twice in the same function
    for i in data_year:
        if i[2] != str('No Data'):
            year.append((i[0],i[4],i[2]))
        list_published_year_freq.append((i[2][0:2]))
        
    
    def century():
        # returns a list of books read, 
        published_year_freq = {}
        for item in list_published_year_freq:
            if item in published_year_freq:
                published_year_freq[item] += 1
            else:
                published_year_freq[item] = 1
        
        print ('\nBelow are the publication dates of the books read, sorted by century:\n ')
        for i in sorted(published_year_freq, key=published_year_freq.get, reverse=True):
            print(i, ": ", published_year_freq[i])
    

    def oldest_youngest():
        # returns the newest and oldest book read    
        author_reversed_new = (' '.join(reversed(year[0][1].split(','))))
        author_reversed_old = (' '.join(reversed(year[-1][1].split(','))))

        print ('\nThe newest book you have read is"', year[0][0], '", Written by', author_reversed_new, 'in the year', year[0][2],',')
        print ('While the oldest book is"', year[-1][0], '", Written by', author_reversed_old, 'in the year', year[-1][2],'.\n ')

    def decade_rating():
        # Haven't been cracked yet - cannt work out the algorithm which adds the decade and adds a rating to a list within that corresponding dictioanry value 

        rating = []
        dict_decade_freq = {}
    
        lists = []
        for i in (data_year):
            
            if i[2] != 'No Data':
                decade = (str(round((int(i[2])/10))*10))
                print (decade)

                dict_decade_freq.update({decade :'x'})
                
            else:
                dict_decade_freq.update({i[2]:'x'})
        
        print (dict_decade_freq)

    
            
    return (century(), oldest_youngest(),end_choices())
    #decade_rating()
  
def quote_puller():
    # gathers data from sql
    data2 = cur.execute('''select * FROM quote_link ''')
    # make a list of the Links
    for i in data2:
        links.append(goodreads_base+i[1])

    quote_files = open(r"quotes.txt", "w", encoding='utf-8')
    count = 0
    print("\nGenerating quotes, please Wait...\n ")

    def writer():
        global complete_quotes
        prog_count = 0
        while True:
            print ('How many quotes do you want to extract?\n ')
            quote_n = (input()) 
            try:
                int_quote_n = int(quote_n)
                print ('Getting', int_quote_n, 'quotes.\n')
                break
            except ValueError:
                print('Invalid input, please try again.\n ')

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
                if count == int_quote_n:
                    break
                # next two lines 1. formats for readability and writes to file
                quote_format_anki = quote.replace('\n', '').replace(
                    '”    ―', '”    <br><br><br>    -')+'\n\n'
                quote_format_txt = quote.replace('\n', '').replace(
                    '”    ―', '”  \n\n\n      -')+'\n\n\n'
                complete_quotes_anki.append(quote_format_anki)
                complete_quotes_txt.append(quote_format_txt)

    #a Appends the quotes to a simple text file.
    def txt_file():
        quote_txt = open('Quotes.txt', 'w')
        for i in complete_quotes_txt:
            quote_txt.write(i)
        print('\n Conversion finished. You will find Quotes.txt file in this directory. \n')
    
    # Takes the scraped quotes and converts them to a format to upload flashcard application anki
    def anki():
        global complete_quotes_anki
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
            'Goodreads Quotes')

        for i in complete_quotes_anki:
            my_note = genanki.Note(
                model=my_model,
                fields=[str(i), ' '])
            my_deck.add_note(my_note)

        genanki.Package(my_deck).write_to_file('Goodreads.apkg')
        print('\nConversion finished. You will find Goodreads.apkg in this directory. \n')


    def file_choice(): 
        while True:
            print('\nDo you want to export the notes to a text file, or to an Anki package?\n\nAnki package (.apkg) = 1 Text File (.txt) = 2')
            file_choice = ((input()))
            if file_choice == str(1):
                print ('Exporting to .apkg. Please wait...')
                anki()
                break
            elif file_choice == str(2):
                print ('Exporting to .txt. Please wait...')
                txt_file()
                break
            else:
               print ("Invalid input. Please try again.")

    return (writer(),file_choice())

def end_choices():
        while True:
            print('\n\nMain menu = 1, Exit program = 2')
            end_choice = ((input()))
            if end_choice == str(1):
                choice()
            elif end_choice == str(2):
                print ('Program terminated.')
                break
            else:
               print ("Invalid input. Please try again.")

def choice():
    choice = 0
    print('Welcome!\nDo you want to see your reading statistics, or do you want to extract the most popular quotes from each book?')
    while True:
        print('\nStatistics = 1\n\nQuotes = 2\n\nExit Program = 3:')
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
        elif choice ==str(3):
            print ('\nProgram terminated.\n')
            break
        else:
            print ("Invalid. Please try again.")

#choice()
#published_year_stats()
#author_stats()
#quote_puller() 
page_stats() 