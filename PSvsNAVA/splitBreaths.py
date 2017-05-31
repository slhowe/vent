def split_breaths(flow):
    """
    Splits the breaths where flow transitions from
    expiration to inspiration.

    Returns list of indices of split points
    """

    indices = []
    pop_indices = []

    # find all indices
    for index in range(1,len(flow)):
        if((flow[index] >= 0) and (flow[index-1] < 0)):
            indices.append(index-1)

    # remove any caused by noise around zero
    MIN_DIFFERENCE = 200
    for pos in range(len(indices)-1):
        if (indices[pos+1] - indices[pos]) < MIN_DIFFERENCE:
            pop_indices.append(pos)
    for pos in reversed(pop_indices):
        indices.pop(pos)

    return indices
