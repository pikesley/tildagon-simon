from time import ticks_ms

from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .lib.background import Background
from .lib.conf import conf
from .lib.panel import Panel


class Simon(app.App):
    """Simon."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)

        self.panels = [Panel(item) for item in conf["panels"]]
        self.last_change = ticks_ms()

        self.sequence = [0, 3, 1, 2, 3]
        # self.sequence = [0]
        self.sequence_index = 0

        self.game_state = "PLAY"

    def update(self, _):
        """Update."""
        for i in range(12):
            tildagonos.leds[i + 1] = (0, 0, 0)

        for panel in self.panels:
            panel.light_leds()

        if self.game_state == "GUESS":
            for panel in self.panels:
                panel.deactivate()
            self.scan_buttons()

        if self.game_state == "PLAY":
            self.play_sequence()

    def play_sequence(self):
        """Play the sequence."""
        self.panels[self.sequence[self.sequence_index]].activate()
        for panel in self.panels:
            panel.deactivate()

        if ticks_ms() - self.last_change > conf["panel"]["intervals"]["activatable"]:
            if self.sequence_index < len(self.sequence) - 1:
                self.sequence_index += 1
            else:
                self.game_state = "GUESS"

            self.last_change = ticks_ms()

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(Background(colour=(0, 0, 0)))

        for panel in self.panels:
            self.overlays.append(panel)

        self.draw_overlays(ctx)

    def scan_buttons(self):
        """Buttons."""
        for panel in self.panels:
            if self.button_states.get(BUTTON_TYPES[panel.button]):
                self.button_states.clear()
                panel.activate()

        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()


__app_export__ = Simon
