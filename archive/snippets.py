def _check_newval_validity(row, col, val_to_test, puzzle):

    """

    A YouTuber's solution:

    """

    for i in range(len(puzzle[0])):  # the [0] is technically unnecessary but here for articulation purposes
        if val_to_test == puzzle[row][i]:
            return False

    # this will count up to 8, where 8 is the *LAST* index in a given row, not 9
    # Here, we manually iterate across the row with the index
    # and check if that value matches with the test value.

    """
    
    Compare this with my own solution:
    
    """

    for i, tile in enumerate(puzzle[row]):
        if tile == val_to_test and col != i:
            return False

    # This is about 10 seconds faster