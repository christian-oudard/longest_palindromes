# Adapted from Fred Akalin at http://www.akalin.cx/longest-palindrome-linear-time

def fast_longest_palindromes(seq):
    """
    Behaves identically to naive_longest_palindromes (see below), but
    runs in linear time.

    >>> fast_longest_palindromes('ababa')
    [0, 1, 0, 3, 0, 5, 0, 3, 0, 1, 0]
    >>> fast_longest_palindromes('yabbadabbadoo')
    [0, 1, 0, 1, 0, 1, 4, 1, 0, 1, 0, 9, 0, 1, 0, 1, 6, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0]
    >>> max(fast_longest_palindromes('a' * 10000))
    10000
    """
    len_seq = len(seq)
    best_lengths = []
    i = 0
    pal_len = 0
    # Loop invariant: seq[(i - pal_len):i] is a palindrome.
    # Loop invariant: len(best_lengths) >= 2 * i - pal_len. The code path that
    # increments pal_len skips the best_lengths-filling inner-loop.
    # Loop invariant: len(best_lengths) < 2 * i + 1. Any code path that
    # increments i past len_seq - 1 exits the loop early and so skips
    # the best_lengths-filling inner loop.
    while i < len_seq:
        # First, see if we can extend the current palindrome.  Note
        # that the center of the palindrome remains fixed.
        if i > pal_len and seq[i - pal_len - 1] == seq[i]:
            pal_len += 2
            i += 1
            continue

        # The current palindrome is as large as it gets, so we append
        # it.
        best_lengths.append(pal_len)

        # Now to make further progress, we look for a smaller
        # palindrome sharing the right edge with the current
        # palindrome.  If we find one, we can try to expand it and see
        # where that takes us.  At the same time, we can fill the
        # values for best_lengths that we neglected during the loop above. We
        # make use of our knowledge of the length of the previous
        # palindrome (pal_len) and the fact that the values of best_lengths for
        # positions on the right half of the palindrome are closely
        # related to the values of the corresponding positions on the
        # left half of the palindrome.

        # Traverse backwards starting from the second-to-last index up
        # to the edge of the last palindrome.
        start = len(best_lengths) - 2
        end = start - pal_len
        for j in range(start, end, -1):
            # d is the value best_lengths[j] must have in order for the
            # palindrome centered there to share the left edge with
            # the last palindrome.  (Drawing it out is helpful to
            # understanding why the - 1 is there.)
            d = j - end - 1

            # We check to see if the palindrome at best_lengths[j] shares a left
            # edge with the last palindrome.  If so, the corresponding
            # palindrome on the right half must share the right edge
            # with the last palindrome, and so we have a new value for
            # pal_len.
            if best_lengths[j] == d: # *
                pal_len = d
                # We actually want to go to the beginning of the outer
                # loop, but Python doesn't have loop labels.  Instead,
                # we use an else block corresponding to the inner
                # loop, which gets executed only when the for loop
                # exits normally (i.end., not via break).
                break

            # Otherwise, we just copy the value over to the right
            # side.  We have to bound best_lengths[i] because palindromes on the
            # left side could extend past the left edge of the last
            # palindrome, whereas their counterparts won't extend past
            # the right edge.
            best_lengths.append(min(d, best_lengths[j]))
        else:
            # This code is executed in two cases: when the for loop
            # isn't taken at all (pal_len == 0) or the inner loop was
            # unable to find a palindrome sharing the left edge with
            # the last palindrome.  In either case, we're free to
            # consider the palindrome centered at seq[i].
            pal_len = 1
            i += 1

    # We know from the loop invariant that len(best_lengths) < 2 * len_seq + 1, so
    # we must fill in the remaining values of best_lengths.

    # Obviously, the last palindrome we're looking at can't grow any
    # more.
    best_lengths.append(pal_len)

    # Traverse backwards starting from the second-to-last index up
    # until we get best_lengths to size 2 * len_seq + 1. We can deduce from the
    # loop invariants we have enough elements.
    size = len(best_lengths)
    start = size - 2
    end = start - (2 * len_seq + 1 - size)
    for i in range(start, end, -1):
        # The d here uses the same formula as the d in the inner loop
        # above.  (Computes distance to left edge of the last
        # palindrome.)
        d = i - end - 1
        # We bound best_lengths[i] with min for the same reason as in the inner
        # loop above.
        best_lengths.append(min(d, best_lengths[i]))

    return best_lengths

# And here is a naive quadratic version for comparison:

def naive_longest_palindromes(seq):
    """
    Given a sequence seq, returns a list best_lengths such that best_lengths[2 * i + 1]
    holds the length of the longest palindrome centered at seq[i]
    (which must be odd), best_lengths[2 * i] holds the length of the longest
    palindrome centered between seq[i - 1] and seq[i] (which must be
    even), and best_lengths[2 * len(seq)] holds the length of the longest
    palindrome centered past the last element of seq (which must be 0,
    as is best_lengths[0]).

    The actual palindrome for best_lengths[i] is seq[start:(start + best_lengths[i])] where start is i
    // 2 - best_lengths[i] // 2. (// is integer division.)

    Example:
    >>> naive_longest_palindromes('ababa')
    [0, 1, 0, 3, 0, 5, 0, 3, 0, 1, 0]
    >>> naive_longest_palindromes('yabbadabbadoo')
    [0, 1, 0, 1, 0, 1, 4, 1, 0, 1, 0, 9, 0, 1, 0, 1, 6, 1, 0, 1, 0, 1, 0, 1, 2, 1, 0]
    >>> max(naive_longest_palindromes('a' * 100))
    100

    Runs in quadratic time.
    """
    len_seq = len(seq)
    size = 2 * len_seq + 1
    best_lengths = []

    for i in range(size):
        # If i is even (i.e., we're on a space), this will produce end
        # == start.  Otherwise, we're on an element and end == start + 1, as a
        # single letter is trivially a palindrome.
        start = i // 2
        end = start + i % 2

        # Loop invariant: seq[start:end] is a palindrome.
        while start > 0 and end < len_seq and seq[start - 1] == seq[end]:
            start -= 1
            end += 1

        best_lengths.append(end - start)

    return best_lengths
