from time import ticks_ms

from app_components import YesNoDialog
from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .lib.background import Background
from .lib.conf import conf
from .lib.high_score_manager import load_high_score, save_high_score
from .lib.panel import Panel
from .lib.scoreboard import Scoreboard
from .lib.sequence_generator import generate_sequence


class Simon(app.App):
    """Simon."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.panels = [Panel(item) for item in conf["panels"]]
        self.reset_timer = 0
        self.score = 0
        self.scoreboard = Scoreboard()
        self.new_game()

    def new_game(self):
        """Clean up ready."""
        self.score = 0
        self.round_count = 0
        self.sequence_length = 2
        self.high_score = load_high_score()
        self.scoreboard = Scoreboard()
        self.reset()

    def reset(self):
        """Restart."""
        self.last_change = ticks_ms()

        if self.round_count % conf["increase-length-after"] == 0:
            self.sequence_length += 1

        self.sequence = generate_sequence(self.sequence_length)
        self.guessed_sequence = []
        self.sequence_index = 0
        self.dialog = None
        self.game_state = "READY"
        self.reset_timer = ticks_ms()

    def exit(self):
        """Quit."""
        self.new_game()
        self.button_states.clear()
        self.minimise()

    def lights_off(self):
        """Kill the lights."""
        for i in range(12):
            tildagonos.leds[i + 1] = (0, 0, 0)

    def update(self, _):  # noqa: C901
        """Update."""
        self.scan_buttons()

        self.lights_off()
        for panel in self.panels:
            panel.light_leds()

        if len(self.guessed_sequence) == len(self.sequence):
            self.round_count += 1
            if self.guessed_sequence == self.sequence:
                self.score += len(self.sequence)
                self.high_score = max(self.score, self.high_score)

                self.reset()
            else:
                save_high_score(self.high_score)
                self.restart_timer = ticks_ms()
                self.dialog = YesNoDialog(
                    message="Play Again?",
                    on_yes=self.new_game,
                    on_no=self.exit,
                    app=self,
                )

        if self.game_state == "READY":
            for panel in self.panels:
                panel.deactivate()
            if ticks_ms() - self.reset_timer > conf["pause-time"]:
                self.scan_ready_buttons()

        if self.game_state == "START-GUESS":
            for panel in self.panels:
                panel.deactivate()
            self.guessed_sequence = []
            self.game_state = "GUESS"

        if self.game_state == "GUESS":
            for panel in self.panels:
                panel.deactivate()
            self.scan_guess_buttons()

        if self.game_state == "PLAY":
            self.play_sequence()

    def play_sequence(self):
        """Play the sequence."""
        if ticks_ms() - self.last_change > conf["panel"]["intervals"]["activatable"]:
            if self.sequence_index <= len(self.sequence):
                self.sequence_index += 1
            else:
                self.game_state = "START-GUESS"
            self.last_change = ticks_ms()

        if self.sequence_index <= len(self.sequence):
            for panel in self.panels:
                panel.deactivate()
            self.panels[self.sequence[self.sequence_index - 1]].activate()

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(Background(colour=(0, 0, 0)))

        for panel in self.panels:
            self.overlays.append(panel)

        if self.scoreboard.scores["score"] < self.score:
            self.scoreboard.scores["score"] += 1
        self.scoreboard.scores["high-score"] = self.high_score
        self.overlays.append(self.scoreboard)

        self.draw_overlays(ctx)

        if self.dialog:
            self.dialog.draw(ctx)

    def scan_guess_buttons(self):
        """Buttons for Guessing stage."""
        for index, panel in enumerate(self.panels):
            if self.button_states.get(BUTTON_TYPES[panel.button]):
                self.button_states.clear()
                panel.activate()
                self.guessed_sequence.append(index)

    def scan_ready_buttons(self):
        """Buttons for Ready stage."""
        for panel in self.panels:
            if self.button_states.get(BUTTON_TYPES[panel.button]):
                self.button_states.clear()
                self.game_state = "PLAY"

    def scan_buttons(self):
        """Always scan here."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()


__app_export__ = Simon
