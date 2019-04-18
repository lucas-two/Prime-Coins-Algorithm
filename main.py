"""
Prime-Coin Change Problem (ver 1.0)
Author: Lucas Geurtjens (s5132841)
18/04/19
"""

import time
import math
import os
import sys


def prime_coins_rec(amount, current_coin, coins_used, coins_lower, coins_upper, param_type):
    """
    Recursive implementation of the prime coin change problem (using DFS)
    :param amount: Amount to pay in coins
    :param current_coin: Which coin should we start from? (avoids combination duplicates)
    :param coins_used: How many coins have been used?
    :param coins_lower: Lower limit or exact amount of coins to be used.
    :param coins_upper: Upper limit of coins to be used.
    :param param_type: Type of parameters being used (1, 2 or 3 inputs)
    :return: An integer sum of no. of solutions found.
    """

    # Find any amount of coins to reach the amount
    if param_type == 1:
        if amount == 0:  # Amount reached 0, hence a solution.
            return 1

        elif amount < 0:  # Amount is less than 0, hence not a solution
            return 0

    # Find an exact amount of coins to reach the amount
    elif param_type == 2:
        # Amount reached 0 and has correct number of coins, hence solution.
        if amount == 0 and coins_used == coins_lower:
            return 1

        # Amount is below 0 or has used too many coins, hence not solution.
        elif amount < 0 or coins_used > coins_lower:
            return 0

    # Find an amount of coins within a range to reach the amount
    elif param_type == 3:
        # Amount reached 0 and has correct number of coins, hence solution.
        if amount == 0 and coins_lower <= coins_used <= coins_upper:
            return 1

        # Amount is below 0 or has used used coins above the range, hence not solution.
        elif amount < 0 or coins_used > coins_upper:
            return 0

    # Otherwise, If we haven't reached a base case
    solutions = 0  # Solutions we have found where amount == 0

    # Recursively loop though coin combinations to find solutions
    # This essentially acts like a pruned DFS (Depth First Search).
    for coin in range(current_coin, len(my_coins)):
        solutions += (prime_coins_rec(amount - my_coins[coin], current_coin, coins_used + 1, coins_lower, coins_upper, param_type))
        current_coin += 1  # Start from the next coin (to avoid duplicates)

    return solutions


def prime_coins_dyn(amount, coins, coins_lower, coins_upper):
    """
    NOTE: Function is not used (implementation is poorly made and not efficient).
    Dynamic implementation of coin change problem (using BFS)
    :param amount: A given amount we will find coins to equal
    :param coins: Our selection of coins to use
    :param coins_lower: Lower limit or exact amount of coins
    :param coins_upper: Upper limit of coins to be used
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
    NOTE: Function is not used (from the dynamic implementation).
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


def main():
    """
    Main of the program.
    """
    try:
        abs_location = os.path.abspath(sys.argv[1])  # Location of input file

    except IndexError:
        print("Error, program must be run from the commandline with arguments.")
        sys.exit(-1)

    try:
        input_f = open(abs_location, "r")

    except FileNotFoundError:
        print("Error: It appears that the input text file location (absolute location) was incorrect.")
        sys.exit(-1)

    # Check which parameters are being used
    for line in input_f:
        arguments = line.split()
        argument_size = len(arguments)

        if argument_size == 1:
            my_amount = int(arguments[0])
            lower_limit = 0
            upper_limit = 0
            my_param = 1

        elif argument_size == 2:
            my_amount = int(arguments[0])
            lower_limit = int(arguments[1])
            upper_limit = 0
            my_param = 2

        elif argument_size == 3:
            my_amount = int(arguments[0])
            lower_limit = int(arguments[1])
            upper_limit = int(arguments[2])
            my_param = 3

        else:
            print("Error, invalid input arguments")
            break

        global my_coins
        my_coins = create_coins(my_amount)

        # Execute algorithm
        start_time = time.time()
        solution_count = prime_coins_rec(my_amount, 0, 0, lower_limit, upper_limit, my_param)
        end_time = time.time()

        print("(%s %s %s) %s solutions found in %0.5f secs" % (my_amount, lower_limit, upper_limit, solution_count, end_time - start_time))

        # Output solutions
        output_f = open("output.txt", "a")
        output_f.write("%s\n" % solution_count)
        output_f.close()

    input_f.close()


if __name__ == "__main__":
    main()