from itertools import islice
import euler_tools

max_div_count = 0
for t in islice(euler_tools.find_triangle_numbers(10000), 10000):

    print t,
    div_count = len(list(euler_tools.find_divisors(t)))
    print div_count

    if div_count > 500:
        break
