import math

def prime(n):
  if n == 1:
    return False
  
  # NOTE: The limit starts at +2 to avoid issues with 2 to sqrt(2) = 1 range in the loop
  limit = 2 + round(math.sqrt(n))
  
  # Check if n is divisible by any other number (hence will not be prime)
  for i in range(2, limit):
    if n % i == 0: 
        return False
    return True
