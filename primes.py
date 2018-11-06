"""
Rolf Vidar Hoksaas
For learning purposes
Run as $ python primes.py [ number [arguments] ]
Arguments:
    --isprime :   Check if number is prime
    --max :       Find primes up until this number
    --counter:    Find this many primes
Default:
    python primes.py 100 --counter
"""

from sys import argv
from random import randint
errorstring = """Run as $ python primes.py [ number [argument] [wait] ]
Arguments:
    --isprime:  Check if number is prime
    --max :     Find primes up until this number
    --counter:  Find this many primes
    --v:        Print primes as found, instead of waiting to print at end
                Only works with --counter and --max
Default:
    python primes.py 100 --counter"""



def add_prime(list_of_primes):
    """
        Add a prime to the given list
        Args:
            list_of_primes: list of N elements
        Returns:
            list_of_primes: list of N+1 elements
    """

    lastPrime = list_of_primes[len(list_of_primes)-1]  # Easier to read
    prime_not_found = True  # Restart for new prime
    testInteger = 0  # Start from first integer after

    while prime_not_found:
        not_a_prime = False
        testInteger += 1
        for i in range(len(list_of_primes)):  # Check for all previous numbers
            if (lastPrime+testInteger) % list_of_primes[i] == 0:  # If composite
                not_a_prime = True  # Must skip
                break  # No point trying the rest
        if not_a_prime == False:  # When all previous primes checked, check if still candidate
            list_of_primes.append(lastPrime+testInteger)  # If so, add it and success!
            prime_not_found = False  # End loop

    return list_of_primes



def max_primes(list_of_primes, cap, wait):
    """
    Function to find all primes up to given number. 
    Args:
        list_of_primes:     Array with primes
        cap:                Highest number to check (number)
    Returns: 
        list_of_elements:   Array with all numbers
    """

    while list_of_primes[-1] < int(cap):  # For as long as last prime is lower than requested
        add_prime(list_of_primes)
        if not wait:
            print(list_of_primes[-1])
    if list_of_primes[-1] > int(cap):
        list_of_primes = list_of_primes[:-1]

    return list_of_primes



def is_prime(list_of_primes, number):
    """
    Function to check if given number is prime.
    Args: 
        list_of_primes: Array with primes
        number:         Requested number
    Returns: 
        True: Number is prime
        False: Number is not prime
    """

    found_prime = False  # Assume it's not prime

    # Special cases
    if int(number) == 1:  # If in array already, end
        # Schrödinger case
        found_prime = True
        schrodinger_factor = randint(0,1)
        if schrodinger_factor:
            return True
        else: 
            return False
    if int(number) == 2 or int(number)== 3:  # If in array already, end
        found_prime = True
        return True

    while list_of_primes[-1] < int(number):  # For as long as last prime is lower than requested
        add_prime(list_of_primes)  # Add more primes
        if list_of_primes[-1] == int(number):  # Check if added prime is the requested one
            return True
            found_prime = True  # Mark as found if so
    if not found_prime:  # When we have checked all previous primes, the number can't be prime
        return False



def count_primes(list_of_primes, how_many, wait):
    """
        Function to find N many primes.
        Args: 
            list_of_primes: Array with primes
            how_many:       Number of primes we want
        Returns:
            list_of_primes: Array with primes
    """
    print(list_of_primes, how_many, wait)
    while len(list_of_primes) < int(how_many):  # For as long as we have less primes than requested
        add_prime(list_of_primes)
        if not wait:
            print(list_of_primes[-1])
    return list_of_primes




def primes(number=100, type="--counter", wait=True):  # Set 100 and counter as default arguments of function
    """
    Function to handle input
    Args:
        number: Number to use, depending of case
        type:   Request to handle
    Return
        None: Script finished
    """

    list_of_primes = [2, 3]  # Start an array of primes with two elements


    if type=="--max" or type=="--m":
        max_primes(list_of_primes, number, wait)
        if wait:
            print(list_of_primes)


    elif type=="--isprime" or type=="--prime" or type=="--p":
        if is_prime(list_of_primes, number):
            print(number, "is prime")
        else:
            print(number, "is not prime")


    elif type=="--counter" or type=="--c":
        count_primes(list_of_primes, number, wait)
        if wait:
            print(list_of_primes)

    return None 



if __name__ == '__main__':
    """
        Initialise script from command line
        Args:
            argv:   captured from sys, from command line
        Return:
            null
    """
    if len(argv) == 2:  # If one parameter is added, include it
        primes(argv[1])
    elif len(argv) == 3:  # Two parameters
        primes(argv[1], argv[2])
    elif len(argv) == 4:
        if (argv[3] == "--verbose" or argv[3] == "--v") and (argv[2] == "--max" or argv[2] == "--m" or argv[2] == "--c" or argv[2] == "--counter"):
            primes(argv[1], argv[2], False)
        else:
            print(errorstring)
    elif len(argv) > 4:
        print(errorstring)
    else:  # No parameters
        primes()


## end
