def choice():
    print('Do you want to see your reading statistics, or do you want to extract the most popular quotes from each book?\n Statistics = 1, Quotes = 2:')
    choice == (int(input()))

    if choice == 1:
        page_stats(data)
    elif choice == 2:
        return quote_puller(data)
    else:
        print (choice)
    print(choice)

choice()

num = input('Enter a number: ')
print(num)
