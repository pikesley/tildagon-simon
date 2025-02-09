from .asset_path import ASSET_PATH


def load_high_score():
    """Load the high-score."""
    try:
        with open(ASSET_PATH + "high.score") as hs:  # noqa: PTH123
            return int(hs.read().strip())
    except:  # noqa: E722
        return 0


def save_high_score(score):
    """Save the high-score."""
    with open(ASSET_PATH + "high.score", "w") as hs:  # noqa: PTH123
        hs.write(str(score))
