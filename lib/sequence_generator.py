from random import randint


def generate_sequence(length):
    """Generate a random sequence."""
    return [randint(0, 4) for _ in range(length)]
