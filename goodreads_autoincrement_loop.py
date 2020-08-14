page_no = range(1,50)
for i in page_no:
    url = requests.get('https://www.goodreads.com/review/list/25345239-oliver?utf8=%E2%9C%93&utf8=%E2%9C%93&order=d&shelf=read&sort=date_added&view=table&title=oliver&per_page=infinite&page=' + str(i))
    soup = BeautifulSoup(url.text, 'lxml')