from math import pi

from .conf import conf


class Scoreboard:
    """Write the score."""

    def __init__(self):
        """Construct."""
        self.score = 0
        self.reset_colours()

    def reset_colours(self):
        """Set colours."""
        self.colours = {
            "background": conf["scoreboard"]["colours"]["background"],
            "text": conf["scoreboard"]["colours"]["text"],
        }

    def invert_colours(self):
        """Invert colours."""
        self.colours = {
            "background": conf["scoreboard"]["colours"]["text"],
            "text": conf["scoreboard"]["colours"]["background"],
        }

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rgb(*self.colours["background"])
        ctx.arc(
            0,
            0,
            conf["scoreboard"]["radius"],
            0,
            pi * 2,
            True,  # noqa: FBT003
        )
        ctx.fill()

        ctx.move_to(0, 0)
        ctx.rgb(*self.colours["text"])
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = conf["scoreboard"]["font-size"]
        ctx.text(str(self.score))
