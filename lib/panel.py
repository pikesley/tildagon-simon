from math import radians

from ..pikesley.rgb_from_hue.rgb_from_hue import rgb_from_hue
from .conf import conf


class Panel:
    """Panel."""

    def __init__(self, angle, hue, opacity=0.7):
        """Construct."""
        self.angle = angle
        self.hue = hue
        self.colour = list(rgb_from_hue(hue)) + [opacity]

    def draw(self, ctx):
        """Draw ourself."""
        semi_arc = conf["panel"]["arc"] / 2
        ctx.rotate(radians(self.angle))
        ctx.rgba(*self.colour)
        ctx.arc(
            0,
            0,
            conf["panel"]["radius"],
            radians(semi_arc),
            radians(-semi_arc),
            True,  # noqa: FBT003
        )
        ctx.arc(
            0,
            0,
            conf["panel"]["radius"] - conf["panel"]["depth"],
            radians(-(semi_arc - 1)),
            radians(semi_arc - 1),
            False,  # noqa: FBT003
        )
        ctx.close_path()

        ctx.fill()
