from bs4 import BeautifulSoup
import grequests
import requests
import  re


links = []
quotes = []


#loads the read shelves
with open('C:\\Users\\Oliver\\desktop\\code_files\\coursera\\Capstone\\02_Exploring_Data\\Goodreads\\Goodreads_read_100.html', 'r', encoding="utf8") as website:
    filez = website.read()
    soupz = BeautifulSoup(filez, 'lxml')

for book in soupz.find_all('tr', class_='bookalike review'):
    name = book.find('td', class_='field title').div.a.text.lstrip().rstrip().strip('\n')
    links.append(book.find('td', class_='field title').div.a.get('href'))
    #print (links)

#grequests initialiser
reqs = (grequests.get(link) for link in links)
resp = grequests.imap(reqs, grequests.Pool(5))

    #quote puller 
# for i in resp:
#     soups = BeautifulSoup(i.text, 'lxml')
#     soups2 = soups.find_all('a', attrs={'href': re.compile("^/work/quotes")})
#     for j in soups2:
#         #quotes.append(j.get('href', 1))
#         links = j.get('href', 1).strip('\n')

    
               
#         quotes = (list(dict.fromkeys(quotes)))
            #print (name, quotes[])

for i in resp:
    soups = BeautifulSoup(i.text, 'lxml')
    for j in  soups.find_all('a',class_='actionLink', attrs={'href': re.compile("^/work/quotes")}):
        print(j.get('href'))

    
               



