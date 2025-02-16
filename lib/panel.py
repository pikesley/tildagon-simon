from math import radians
from time import ticks_ms

from events.input import BUTTON_TYPES
from tildagonos import tildagonos

from ..pikesley.rgb_from_hue.rgb_from_hue import rgb_from_hue
from .conf import conf
from .gamma import gamma_corrections


class Panel:
    """Panel."""

    count = 0

    def __init__(self, data):
        """Construct."""
        self.index = self.count
        self.angle = data["angle"]
        self.hue = data["hue"]
        self.leds = data["leds"]
        self.button = BUTTON_TYPES[data["button"]]
        self.colours = {
            "plain": list(rgb_from_hue(self.hue))
            + [conf["panel"]["opacities"]["plain"]],
            "border": list(rgb_from_hue(self.hue))
            + [conf["panel"]["opacities"]["border"]],
            "active": list(rgb_from_hue(self.hue))
            + [conf["panel"]["opacities"]["active"]],
        }
        self.colour = self.colours["plain"]
        self.semi_arc = conf["panel"]["arc"] / 2

        self.active = False
        self.ready = True
        self.activation_timer = 0

        Panel.count += 1

    def draw(self, ctx):
        """Draw ourself."""
        ctx.rotate(radians(self.angle))

        ctx.rgba(*self.colours["plain"])
        if self.active:
            ctx.rgba(*self.colours["active"])

        self.make_shape(ctx)
        ctx.fill()

        ctx.rgba(*self.colours["border"])
        self.make_shape(ctx)
        ctx.stroke()

    def make_shape(self, ctx):
        """Make the shape."""
        ctx.arc(
            0,
            0,
            conf["panel"]["radius"],
            radians(self.semi_arc),
            radians(-self.semi_arc),
            True,  # noqa: FBT003
        )
        ctx.arc(
            0,
            0,
            conf["panel"]["radius"] - conf["panel"]["depth"],
            radians(-(self.semi_arc - conf["panel"]["shim"])),
            radians(self.semi_arc - conf["panel"]["shim"]),
            False,  # noqa: FBT003
        )
        ctx.close_path()

    def light_leds(self):
        """Light our LEDs."""
        colour = rgb_from_hue(self.hue)
        brightness = conf["leds"]["brightness"]["default"]
        if self.active:
            brightness = conf["leds"]["brightness"]["active"]

        for index in self.leds:
            tildagonos.leds[index] = [
                gamma_corrections[int(c * 255 * brightness)] for c in colour
            ]

    def activate(self):
        """Briefly activate ourself."""
        if not self.active and self.ready:
            self.active = True
            self.activation_timer = ticks_ms()
            self.ready = False

    def deactivate(self):
        """Should we turn off."""
        if (
            ticks_ms() - self.activation_timer
            > conf["panel"]["intervals"]["activation"]
        ):
            self.active = False

        if (
            ticks_ms() - self.activation_timer
            > conf["panel"]["intervals"]["activatable"]
        ):
            self.ready = True
