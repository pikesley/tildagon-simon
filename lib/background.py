class Background:
    """Background."""

    def __init__(
        self,
    ):
        """Construct."""

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
