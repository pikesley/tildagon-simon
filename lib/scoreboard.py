

class Scoreboard:
    """Write the scores."""

    def __init__(self):
        """Construct."""
        self.scores = {"score": 0}

    def draw(self, ctx):
        """Draw ourself."""
        ctx.move_to(0, 0)
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = 60
        ctx.text(str(self.scores["score"]))
