
This was created to both test and display a number of competencies i have been learning, such as:
- Use of HTML parsing/scraping via packages such as Beautiful Soup or Requests
- Database construction and management using SQLite
- Constructing and writing a multi file project, allowing python to read and write to/from external sources
- General algorithmic complexity


________________________________________________________________________________________________
This project locates a user's read lists from Goodreads and provides two main functions:

1. The first function displays a number of statistics based on the user's read books.
The statistics shows such information such as :
- The average page count of a book
- The proportions of the book publishing date by century
- The most books read by each author. 
While rudimentary in complexity, the statistics provided by Goodreads itself is very weak, and did not give the information I wanted to see.
I will update this further with a greater amount of complexity in the future.

2. The second function of this project operates by locating the books' most popular quotes and collating them for further reading. 
The user is able to either:
- Create a deck for Anki, a popular spaced repetition flashcard application; each quote is separately added to a single sided card and added to its own deck.
- It is also possible to simply write the quotes to a single text, or pdf file.

____________________________________________________________________________________________________________________________________________

How To:

The application functions via two Python scripts, each to be executed in order:

1. Running goodreads_pull_master will generate a database:
- The user will be prompted to provide a user ID number; this will be found by directing yourself to your Goodreads read list, and finding the string of numbers found in the URL
at the top of the page. Provided is an example of the authors ID:
' https://www.goodreads.com/review/list/25345239?order=a&shelf=read&sort=date_read&view=table# ' 
- In this case, 25345239 is the user ID code.
- This will generate a SQL database for the user, and will be prompted when finished.

2. After the database is generated, Goodreads_Pull_Master.py may be executed:
- This file extracts the necessary information from the databases, and generates either statistical analysis, or extraction of popular quotes from each text
- In the case of quote extraction, the file will be found in the code directory as 'Goodreads.APKG', for example.

Thank you!

