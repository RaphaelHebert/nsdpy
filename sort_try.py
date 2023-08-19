def merge_and_sort_sequences(sequences):
    if not sequences:
        return []

    # Sort the sequences based on their starting indices
    sequences.sort(key=lambda x: x[0])

    merged_sequences = [sequences[0]]

    for i in range(1, len(sequences)):
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


# Example usage
input_sequences = [(1, 5), (3, 8), (6, 10), (9, 12)]
merged_sorted_sequences = merge_and_sort_sequences(input_sequences)
print(merged_sorted_sequences)

input_sequences2 = [
    (14, 18),
    (19, 32),
    (1, 5),
    (3, 8),
    (6, 10),
    (9, 12),
]
merged_sorted_sequences2 = merge_and_sort_sequences(input_sequences2)
print(merged_sorted_sequences2)
