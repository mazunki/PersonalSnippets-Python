# Rolf Vidar Hoksaas
# For learning purposes
# Run as $ python primes.py [ number [arguments] ]
# Arguments:
# --isprime :   Check if number is prime
# --max :       Find primes up until this number
# --counter:    Find this many primes
# No arguments means 100 primes with --counter


import sys


def add_prime(list_of_primes):  # A callable function to insert a prime to list
    add_to_prime = 0  # Reset counter for next prime

    for ii in range(list_of_primes[len(list_of_primes) - 1]):  # Test for all primes found until now
        if (list_of_primes[len(list_of_primes) - 1] + add_to_prime) % list_of_primes[ii] == 0:  # From last prime upwards test if composite of any other
            add_to_prime += 1  # If not found, try next number
        else:  # If found a prime, add to end of list
            list_of_primes.append(list_of_primes[len(list_of_primes) - 1] + add_to_prime)
            break  # Break this round of primes, to stop adding more. Messed up the counter of primes
    return list_of_primes


def primes(how_many=100, type="--counter"):  # Set 100 as default argument of function

    list_of_primes = [1, 2]  # Start an array of primes with two elements


# Primes until cap

    if type=="--max" or type=="--m":
        while list_of_primes[len(list_of_primes)-1] < int(how_many):  # For as long as last prime is lower than requested
            add_prime(list_of_primes)
        if list_of_primes[len(list_of_primes)-1] > int(how_many):
            list_of_primes = list_of_primes[:-1]
        print(list_of_primes)  # Print end result

# Is prime?

    elif type=="--isprime" or type=="--prime" or type=="--p":
        found_prime = False  # Assume it's not prime
        if int(how_many) == 1:  # If in array already, end
            print("Schrödinger")
            found_prime = True
        if int(how_many) == 2:  # If in array already, end
            print("Yep, prime")
            found_prime = True

        while list_of_primes[len(list_of_primes)-1] < int(how_many):  # For as long as last prime is lower than requested
            add_prime(list_of_primes)
            if list_of_primes[len(list_of_primes)-1] == int(how_many):
                print("Prime number")
                found_prime = True  # Mark as found if so
        if not found_prime:
            print("Not prime")

# Count primes found!

    elif type=="--counter" or type=="--c":
        while len(list_of_primes) < int(how_many):  # For as long as we have less primes than requested
            add_prime(list_of_primes)
        print(list_of_primes)  # Print end result



# Initialise script

if __name__ == '__main__':
    if len(sys.argv) == 2:  # If one parameter is added, include it
        primes(sys.argv[1])
    elif len(sys.argv) == 3:  # Two parameters
        primes(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 3:
        print("\n# Run as $ python primes.py [ number [arguments] ]\n# Arguments:\n# --isprime :   Check if number is prime\n# --max :       Find primes up until this number\n# --counter:    Find this many primes\n#\n# No arguments means 100 primes with --counter")
    else:  # No parameters
        primes()

## end
