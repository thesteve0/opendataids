
## Use this
## http://gbdxtools.readthedocs.io/en/latest/user_guide.html

def run_numbers():
    #pull in catids
    #get bbox and date for each catid and associate it with the catid
    #sort on date and then x1
    #then a bunch of if statements to determine project
    with open('open-data-catids.txt') as f:
        for line in f:
            print(line.strip())
    print("hello world")


run_numbers()