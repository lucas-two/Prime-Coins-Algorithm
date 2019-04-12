"""
Prime-Coin Problem v0.1A 12/04/19

GOALS:
- Implement a way to calculate a set of prime numbers
for our coins. We are currently doing this statically.

- Implement a maximum/range of coins we want to be used
 for a given amount.

 - Make our function behave recursively.
"""

import time


def prime_coins(amount, coins):
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

        # If we've met the exact amount, return this as a solution
        if current_amount == amount:
            solutions.append(node)
            print("SOLUTION: %s" % node)

        # Otherwise, look at the node's children (ONLY if it's total is less than the current amount)
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


amount_test = 5
coins_test = [1, 2, 3, 5]

start_time = time.time()
solution = prime_coins(amount_test, coins_test)
end_time = time.time()

print("%s solutions found in %.5f secs" % (len(solution), end_time - start_time))
