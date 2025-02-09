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

        ctx.move_to(-75, -55)
        ctx.text_baseline = ctx.BOTTOM
        ctx.font_size = 10
        ctx.text("high score")

        ctx.move_to(-75, -50)
        ctx.text_baseline = ctx.TOP
        ctx.font_size = 40
        ctx.text(str(self.scores["high-score"]))
