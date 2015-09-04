"""In this game you have to guess whether the number is a prime or not.

Fun AND educative!
execute primegame.play.__doc__ for more info
"""

import random
from bla import clear

def isprime(n):

    """Check if integer n is a prime."""

    n = abs(int(n)) # make sure n is a positive integer

    if n < 2: # 0 and 1 are not primes

        return False

    if n == 2: # 2 is the only even prime number

        return True

    if not n & 1: # all other even numbers are not primes

        return False

# range starts with 3 and only needs to go up the squareroot of n

    for x in range(3, int(n**0.5)+1, 2): 

        if n % x == 0:

            return False

    return True

def notprime(n):

    """If integer isn't a prime, what is it then?"""

    for x in range(3, int(n**0.5)+1, 2): 

            if n % x == 0:

                return str(n) + ' is the product of ' + str(x) + ' * ' + str(n/x)



def play():

    """Play the game.

    answer 'q' or 'quit' to quit
    """

    line = "----------------------"
    correct = True
    rand_max=10
    number = random.randrange(1,rand_max,2)
    prime = isprime(number)
    level = 1
    score = 0
    turn = 0
    limit = 2

    clear.clear()
    print "\t\t\t\t\tStart!\n\n"

    while correct == True:

        print number, '\n'
        answer=str(raw_input("Is this a prime y/n? "))
        if answer not in ('q', 'n', 'y', '0', 'quit', 'no', 'ye', 'yes', 's', 'stop'):
            print "Please answer in yes or no\n"
            continue
        if answer in ('y', 'ye', 'yes'):
            answer =  True
        if answer in ('n', 'no'):
            answer = False
        if answer in ('s', 'stop', '0'):
            return score
            break
        if answer in ('q', 'quit'):
            exit()

        if answer == prime:
            clear.clear()
            score = score + number
            print "Correct!\n"
            print line+line
            print "Your score is: " + str(score)
            print line+line, "\n"
            turn = turn+1
            if turn >= limit:
                limit = 5*level
                level = level+1
                rand_max = rand_max*10
                print "Level " + str(level) + "!" + "\n"


            correct == True
            number = random.randrange(1,rand_max,2)
            prime = isprime(number)

        elif answer != prime:
            correct == False
            score = 0
            turn = 0
            level = level/2
            rand_max=rand_max/2
            limit = limit/2

            clear.clear()
            if notprime(number) != None:
                print "\nIncorrect! ", notprime(number)

            else:
                print "\nIncorrect! "

            print line+line
            print "Your score is: " + str(score)
            print line+line, "\n"
            print "Level " + str(level) + "!" + "\n"
        
            number = random.randrange(1,rand_max,2)
            prime = isprime(number)
            

if __name__ == "__main__":
    import sys
    play()
