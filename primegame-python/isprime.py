
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

        for x in range(3, int(n**0.5)+1, 2): 

            if n % x == 0:

                return str(n) + ' equals ' + str(x) + ' * ' + str(n/x)
            
