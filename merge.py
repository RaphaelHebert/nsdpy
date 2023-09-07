def merge_and_sort_overlaps(sequences, length):
    if not sequences:
        return []

    forward_sequences = []
    for seq in sequences:
        if seq[2] == "-":
            forward_sequences = forward_sequences + [
                (length + 1 - seq[1], length + 1 - seq[0])
            ]
            continue
        forward_sequences = forward_sequences + [(seq[0], seq[1])]

    # Sort the sequences based on their starting indices
    sequences.sort(key=lambda x: x[0])

    merged_sequences = [sequences[0]]

    for i in range(1, len(sequences[:-1])):
        current_start, current_end = sequences[i]
        last_merged_start, last_merged_end = merged_sequences[-1]

        if current_start <= last_merged_end + 1:
            # Overlapping, merge the sequences
            merged_sequences[-1] = (
                last_merged_start,
                max(last_merged_end, current_end),
            )
        else:
            # Non-overlapping, add to the merged list
            merged_sequences.append((current_start, current_end))

    return merged_sequences


print(merge_and_sort_overlaps([(6847, 8583, "+"), (6847, 8583, "+")], 15417))
