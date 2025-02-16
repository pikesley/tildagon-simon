from random import choice, randint


def generate_sequence(length):
    """Generate a random sequence."""
    candidates = list(range(6))
    sequence = [randint(0, 4)]

    while len(sequence) < length:
        restricted_candidates = candidates[:]
        restricted_candidates.remove(sequence[-1])
        sequence.append(choice(restricted_candidates))

    return sequence
