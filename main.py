"""
Prime-Coin Problem v0.5 12/04/19

GOALS:
 - Let our program accept an input.txt file as input.
 - Get the program running from the command line.
 - Make our function behave recursively.
"""

import time
import math


def prime_coins(amount, coins, coins_lower = 0, coins_upper = 0):
    """
    Using BFS, performs backtracking to find combinations of
    coins to equal a certain amount.
    :param amount: A given amount we will find coins to equal.
    :param coins: Our selection of coins to use
    :return: A list of solutions
    """
    solutions = []
    visited = set()
    queue = []

    # Append initial nodes to the queue
    for node in coins:
        queue.append([node])

    # Do this while we have elements in the queue
    while queue:
        node = queue.pop(0)  # Take off the first node

        # Calculate the total of your current node.
        current_amount = calc_total(node)

        # Amount of coins we have in the list
        coin_count = len(node)

        # Do we have an upper and lower coins parameter?
        if coins_lower != 0 and coins_upper != 0:
            # We have the correct amount and is between the coin range
            if current_amount == amount and coins_lower <= coin_count <= coins_upper:
                solutions.append(node)
                print("SOLUTION: %s" % node)

            # Add more children while we're less than the amount and below max coin limit
            elif current_amount < amount and coin_count <= coins_upper:
                for coin in coins:
                    child = node[:]
                    child.append(coin)
                    child.sort()  # Using a timsort of O(nlogn) complexity.
                    if tuple(child) not in visited:
                        visited.add(tuple(child))
                        queue.append(child)

        # Do we have an exact (lower) parameter?
        elif coins_lower != 0:
            # We have a correct amount and is equal to the coin limit
            if current_amount == amount and coin_count == coins_lower:
                solutions.append(node)
                print("SOLUTION: %s" % node)

            # Add more children while we're less than amount and the coin limit
            elif current_amount < amount and coin_count <= coins_lower:
                for coin in coins:
                    child = node[:]
                    child.append(coin)
                    child.sort()  # Using a timsort of O(nlogn) complexity.
                    if tuple(child) not in visited:
                        visited.add(tuple(child))
                        queue.append(child)

        # Do we have no range parameter?
        else:
            # We have a correct amount
            if current_amount == amount:
                solutions.append(node)
                print("SOLUTION: %s" % node)

            # Add more children while we're less than the amount
            elif current_amount < amount:
                for coin in coins:
                    child = node[:]
                    child.append(coin)
                    child.sort()  # Using a timsort of O(nlogn) complexity.
                    if tuple(child) not in visited:
                        visited.add(tuple(child))
                        queue.append(child)
    return solutions


def calc_total(node):
    """
    Calculates the total cost of a given node.
    :param node: Our current coins we have (node)
    :return: The sum total of all coins it's coins
    """
    total = 0
    for coin in node:
        total += coin
    return total


def prime(n):
    """
    Checks if a given number is prime or not
    :param n: Number to check
    :return: True or False
    """
    # 1 is not prime
    if n == 1:
        return False

    # 2 and 3 are prime.
    if n == 2 or n == 3:
        return True

    # NOTE: We set the range to +2 so that the lower limit is never higher than it.
    # Using sqrt, we can avoid checking multiple factors. e.g. if n = 100, checking to i = 10 is enough.
    limit = 2 + round(math.sqrt(n))

    # Check if n is divisible by any other number (hence will not be prime)
    for i in range(2, limit):
        if n % i == 0:
            return False
    return True


def create_coins(amount):
    """
    Creates the available coins we can use for a given amount
    :param amount: The amount we are given
    :return: A list of coins we can use
    """
    available_coins = []
    available_coins.append(1)  # Include 1 as a coin

    # Check and append prime numbers
    for i in range(1, amount):
        if prime(i):
            available_coins.append(i)

    # Check if our gold coin was already added (was a prime).
    if available_coins[len(available_coins) - 1] != amount:
        available_coins.append(amount)

    return available_coins


my_amount = 8
lwr_coins = 2
upr_coins = 5

start_time = time.time()
solution = prime_coins(my_amount, create_coins(my_amount), lwr_coins, upr_coins)
end_time = time.time()

print("%s solutions found in %0.5f secs" % (len(solution), end_time - start_time))

