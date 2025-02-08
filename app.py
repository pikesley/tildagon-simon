from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .pikesley.rgb_from_hue.rgb_from_hue import rgb_from_hue
from .lib.conf import conf
from .lib.gamma import gamma_corrections
from .lib.background import Background
from .lib.panel import Panel


class Simon(app.App):
    """Simon."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)

    def update(self, _):
        """Update."""
        self.scan_buttons()

        for i in range(12):
            tildagonos.leds[i + 1] = (0, 0, 0)

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(Background(colour=(0, 0, 0)))

        for panel in conf["panels"]:
            self.overlays.append(Panel(
                angle=panel["angle"],
                hue=panel["hue"]
                ))

            colour = rgb_from_hue(panel["hue"])
            for index in panel["leds"]:
                tildagonos.leds[index] = [
                gamma_corrections[int(c * 255 * conf["leds"]["brightness"]["default"])]
                for c in colour
            ]

        self.draw_overlays(ctx)

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()


__app_export__ = Simon
