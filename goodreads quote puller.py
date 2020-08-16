from bs4 import BeautifulSoup
import requests
import  re

url = requests.get('https://www.goodreads.com/book/show/5129.Brave_New_World')
soup = BeautifulSoup(url.text, 'lxml')

for book in soup.find_all('a', attrs={'href': re.compile("^/work/quotes")}):
    print(book.get('href'))



