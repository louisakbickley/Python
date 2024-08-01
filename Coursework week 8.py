# -*- coding: utf-8 -*-
"""
Various operations on a standard deck of 52 playing cards
"""


from random import random

# Problem 1
def new_deck():
    """
    Returns a list of all 52 cards in the order that the cards are typically
    arranged in a new deck (Ace to King of Hearts, Ace to King of Clubs, King 
    to Ace of Diamonds, King to Ace of Spades)
    """
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['♥', '♣', '♦', '♠']
    deck = []
    for i in range(2):
        for j in range(13):
            deck_entry = ranks[j] + suits[i]
            deck.append(deck_entry)
    
    for i in range(2, 4):
        for j in range(13):
            deck_entry = ranks[-(j+1)] + suits[i]
            deck.append(deck_entry)
        
    return deck

# Problem 2
def riffle(d):
    """
    Returns a riffle shuffled version of the list of cards d passed to the 
    function. This is done as follows:
        1) The deck of n cards is cut into two, with the first half of the cards
    in the deck put into list A and the second half of the deck in list B (if n
    is odd, then list B has one more card than list A, otherwise they are of
    equal size).
        2) As long as there are cards remaining in either list:
            - either list A or list B is chosen randomly. The probability that
              list A is chosen is equal to the fraction of the cards remaining 
              that are in list A
            - the first card from the chosen list is moved to the end of the
              shuffled deck
    """
    n = len(d)
    list_a = []
    list_b = []
    if n % 2 == 0:
        list_a = d[:(n//2)]
        list_b = d[(n//2):]
    else:
        list_a = d[:((n-1)//2)]
        list_b = d[((n-1)//2):]
    
    riffle_shuffled_deck = []
    
    while list_a != [] and list_b != []:
        p_list_a = len(list_a)/(len(list_a)+len(list_b))
        if random() < p_list_a:
            riffle_shuffled_deck.append(list_a[0])
            del list_a[0]
        else:
            riffle_shuffled_deck.append(list_b[0])
            del list_b[0]
    
    riffle_shuffled_deck.extend(list_a)
    riffle_shuffled_deck.extend(list_b)
        
    return riffle_shuffled_deck

# Problem 3
def deal(d, n):
    """
    Takes a list of cards d and some positive integer number of players n, and
    returns a list of n elements, each of which contains a list of the cards in
    each players hand
    """
    final_list = []
    
    for i in range(n):
        list_i = []
        if len(d) % n == 0:
            for j in range(i, len(d), n):
                list_i.append(d[j])
        else:
            for j in range(i, len(d)-len(d)%n, n):
                list_i.append(d[j])
        final_list.append(list_i)
        
    return final_list

# Problem 4
def hand_string(h):
    """
    takes a list of cards h and returns a string containing each card, sorted 
    firstly by suit in order ♥, ♣, ♦, ♠, then in ascending rank order, with 
    each card separated by a space
    """
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['♥', '♣', '♦', '♠']
    hand_list = []
    
    for j in suits:
        for i in ranks:
            if i+j in h:
                hand_list.append(i+j)
                
    return " ".join(hand_list)                

# main() function for all the testing
def main():
    print(new_deck())
    print(riffle(['A♥', '2♥', '3♥', '4♥']))
    print(riffle(['A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥']))
    print(riffle(new_deck()))
    print(deal(['A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥'], 3))
    print(deal(['A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥'], 1))
    print(deal(['A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'K♦', 'Q♦', 'J♦', '10♦', '9♦', '8♦', '7♦', '6♦', '5♦', '4♦', '3♦', '2♦', 'A♦', 'K♠', 'Q♠', 'J♠', '10♠', '9♠', '8♠', '7♠', '6♠', '5♠', '4♠', '3♠', '2♠', 'A♠'], 5))
    print(hand_string(['A♣', '2♦', '10♠', '4♥', 'A♦', '6♠', '7♣', 'K♥', '9♥']))

main() # call main() function to run all tests