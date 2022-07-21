# Problem 68:
#     Magic 5-gon Ring
#
# Description:
#     Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.
#         [https://projecteuler.net/project/images/p068_1.png]
#
#     Working clockwise,
#       and starting from the group of three with the numerically lowest external node (4,3,2 in this example),
#       each solution can be described uniquely.
#     For example, the above solution can be described by the set: 4,3,2; 6,2,1; 5,1,3.
#
#     It is possible to complete the ring with four different totals: 9, 10, 11, and 12.
#     There are eight solutions in total.
#
#         | Total |    Solution Set     |
#         |-------|---------------------|
#         |   9	  | 4,2,3; 5,3,1; 6,1,2 |
#         |   9	  | 4,3,2; 6,2,1; 5,1,3 |
#         |  10	  | 2,3,5; 4,5,1; 6,1,3 |
#         |  10	  | 2,5,3; 6,3,1; 4,1,5 |
#         |  11	  | 1,4,6; 3,6,2; 5,2,4 |
#         |  11	  | 1,6,4; 5,4,2; 3,2,6 |
#         |  12	  | 1,5,6; 2,6,4; 3,4,5 |
#         |  12	  | 1,6,5; 3,5,4; 2,4,6 |
#
#     By concatenating each group it is possible to form 9-digit strings;
#       the maximum string for a 3-gon ring is 432621513.
#
#     Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit strings.
#     What is the maximum 16-digit string for a "magic" 5-gon ring?

from itertools import permutations
from typing import List, Tuple


def main(n: int) -> Tuple[List[str], str]:
    """
    Returns all the unique solutions for a magic `n`-gon ring,
      as well as the maximum concatenated solution among those.

    Args:
        n (int): Natural number in range [3, 5]

    Returns:
        (Tuple[List[str], str]):
            Tuple of ...
              * List of all unique solutions for a magic `n`-gon ring
              * Maximum concatenated solution among those

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and 3 <= n <= 5

    # Idea:
    #     Probably would be better to DFS through solutions and satisfy constraints along the way.
    #     But the number of potential solutions isn't that much,
    #       so just iterate through all permutations and check the constraints for validity.
    #     Skip any orderings which are not the unique description, to avoid redundancy.
    #
    #     Represent the ring simply as an array of size `2n`.
    #     First half of array, (n elements) will be the external nodes in clockwise order.
    #     The unique representation requires the first element of those to be the least,
    #       so if element at index `0` is not the least, then skip that permutation.
    #
    #     Latter half of array will be the internal nodes.
    #
    #     For some index `i` in left half of array,
    #       the internal nodes lined up with it will be at index (n + i) and (n + (i+1)%n)

    # Possible entries in ring
    entries = list(range(1, 2*n+1))

    # Lines in magic ring (represented by position in ring array)
    #   which must have the same sum
    constraints = [(i, n+i, n + (i+1) % n) for i in range(n)]

    sol_strs = []
    sol_concat_max = 0
    for ring in permutations(entries):
        # Specific constraint for n = 5,
        #   where concatenated solution must be 16 digits,
        #   meaning 10 must be an external node.
        if n == 5 and 10 not in ring[:n]:
            continue

        # Maintain uniqueness of solutions by having the least external node be the first one
        if min(ring[:n]) != ring[0]:
            continue

        # Check if constrained lines each sum to same value
        lines = list(map(lambda c: list(map(lambda i: ring[i], c)), constraints))
        sums = set(map(sum, lines))
        if len(sums) > 1:
            continue

        sol_concat = int(''.join([str(x) for line in lines for x in line]))
        sol_concat_max = max(sol_concat_max, sol_concat)

        sol_str = '; '.join(map(lambda line: ','.join(map(str, line)), lines))
        sol_strs.append(sol_str)

    sol_strs.sort(reverse=True)
    return sol_strs, sol_concat_max


if __name__ == '__main__':
    magic_ring_size = int(input('Enter a natural number (in range [3, 5]): '))
    magic_ring_solutions, magic_ring_solution_max = main(magic_ring_size)
    print('Solutions for a magic {}-gon ring:'.format(magic_ring_size))
    for magic_ring_solution in magic_ring_solutions:
        print('  {}'.format(magic_ring_solution))
    print()
    print('Maximum solution string:')
    print('  {}'.format(magic_ring_solution_max))
