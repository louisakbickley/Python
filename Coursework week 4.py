# -*- coding: utf-8 -*-
"""
Various mathematical operations
"""

import math

def is_prime(n):
    """
    Returns `True` if `n` is a prime number and `False` otherwise.
    This was problem 3 of the week 3 home exercises.
    """
    if n < 2:
        return False
    for k in range(2, n):
        if n % k == 0:
            return False
    return True

# Problem 1
def limiter(a, b, limitertype="ARITHM"):
    """
    Accepts two float arguments a and b and a string limitertype
    Returns a float value resulting from the appropriate type of slope limiter
    function applied to the float values a and b
    If limitertype is set to "WENO", the value of WENO(a,b) is returned
    If limitertype is set to "MINMOD", the value of MINMOD(a,b) is returned
    If limitertype is not specified, the arithmetic mean of a and b is returned
    """
    def w(d):
        w_answer = 1/(math.pow(d, 2) + math.pow(10, -6))
        return w_answer
    
    def WENO(a, b):
        weno_answer = (w(a)*a + w(b)*b)/(w(a) + w(b))
        return weno_answer
    
    def MINMOD(a, b):
        if a == abs(a) and b == abs(b):
           return min(2*a, 2*b, (a + b)/2) 
        elif a != abs(a) and b != abs(b):
            return max(2*a, 2*b, (a + b)/2)
        else:
            return 0
        
    def ARITHM(a,b):
        arithm_answer = (a + b)/2
        return arithm_answer
            
    if limitertype == "WENO":
        return WENO(a, b)
    elif limitertype == "MINMOD":
        return MINMOD(a, b)
    else:
        return (ARITHM(a,b))
    
    
# Problem 2
def pow_mod(a, b, c):
    """
    Accepts positive integer arguments a, b and c 
    Returns the remainder when a^b is divided by c
    """     
    return a**b % c


# Problem 3
def two_knodel(m):
    """
    Accepts an integer argument m
    Returns 'True' if m is a 2-Knodel number and 'False' otherwise
    """  
    if m <= 2:
        return False 
    elif is_prime(m) == True:
        return False
    else:
        for i in range(1, m):
            if math.gcd(i, m) == 1 and pow_mod(i, m-2, m) != 1:
                    return False
    return True

# main() function for all the testing
def main():
    print("should return 0:   ", limiter(-3, 4, 'MINMOD'))
    print("Should return 3.5: ", limiter(3, 4, 'MINMOD'))
    print("should return 0.120001...:   ", limiter(0.1, 0.2, 'WENO'))
    print("should return -0.95: ", limiter(5.4, -7.3))
    print("should return 5...:   ", pow_mod(3, 5, 7))
    print("should return 0: ", pow_mod(5, 6, 5))
    print("should return False:  ", two_knodel(9))
    print("should return True:  ", two_knodel(10))
    print("should return False:  ", two_knodel(3))
    print("should return True:  ", two_knodel(94))
    
main() # call main() function to run all tests