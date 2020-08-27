print('''please provide your user id.\n 
            this can be found when directing to your user profile, 
            and locating a string of numbers in the url at the top of the page. ''')


while True:
    try:
        user_id = int(input('Enter your id:'))
        break
    except ValueError:
        print ("Invalid id. Try again")
            

print (user_id)