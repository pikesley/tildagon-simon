from time import ticks_ms

import imu
from app_components import YesNoDialog
from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable

import app

from .lib.background import Background
from .lib.conf import conf
from .lib.game_board import GameBoard
from .lib.scoreboard import Scoreboard
from .lib.sequence_generator import generate_sequence


class Simon(app.App):
    """Simon."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        self.pause_timer = 0
        self.button_states = Buttons(self)
        self.score = 0
        self.game_board = GameBoard()
        self.scoreboard = Scoreboard()

        self.timers = {
            "pause-before-scoring": {"value": None, "duration": conf["pause-time"]},
            "restart": {"value": None, "duration": conf["pause-time"]},
            "next-round": {"value": None, "duration": conf["pause-time"]},
            "play": {"value": None, "duration": conf["pause-time"]},
        }
        self.new_game()

    def new_game(self):
        """Clean up ready."""
        self.score = 0
        self.round_count = 0
        self.sequence_length = conf["game"]["starting-sequence-length"]
        self.scoreboard = Scoreboard()
        self.reset()

    def reset(self):
        """Restart."""
        self.unset_timers()
        self.set_timer("restart")
        self.lengthen_sequence()
        self.scoreboard.reset_colours()

        self.sequence = generate_sequence(self.sequence_length)
        self.guessed_sequence = []
        self.sequence_index = 0
        self.dialog = None
        self.set_game_state("READY")
        self.pause_timer = None

        self.shaken_values = []

    def lengthen_sequence(self):
        """Make the sequences longer."""
        if (
            self.round_count > 0
            and self.round_count % conf["increase-length-after"] == 0
        ):
            self.sequence_length += 1

    def exit(self):
        """Quit."""
        self.new_game()
        self.button_states.clear()
        self.minimise()

    def shaken(self):
        """Have we been shaken?"""
        self.shaken_values.append(max(abs(g) for g in imu.gyro_read()))
        self.shaken_values = self.shaken_values[-3:]
        return all(v > conf["shake-threshold"] for v in self.shaken_values[-3:])

    def update(self, _):  # noqa: C901
        """Update."""
        for panel in self.game_board.panels:
            panel.light_leds()
            panel.deactivate()

        if self.game_state == "READY" and self.timer_expired("restart"):
            self.scan_ready_buttons()

        if self.game_state == "NEXT-ROUND":
            self.scoreboard.invert_colours()
            if self.timer_expired("next-round"):
                self.set_timer("play")
                self.set_game_state("PLAY")

        if self.game_state == "PLAY":
            self.scoreboard.reset_colours()
            if self.timer_expired("play"):
                self.play_sequence()

        if self.game_state == "GUESS":
            self.scan_guess_buttons()

        if not self.timers["pause-before-scoring"]["value"] and len(
            self.guessed_sequence
        ) == len(self.sequence):
            self.set_timer("pause-before-scoring")
            self.set_game_state("SCORING")

        if self.timer_expired("pause-before-scoring") and self.game_state == "SCORING":
            self.round_count += 1
            if self.guessed_sequence == self.sequence:
                self.score += len(self.sequence)
                self.reset()

            else:
                self.dialog = YesNoDialog(
                    message="Play Again?",
                    on_yes=self.new_game,
                    on_no=self.exit,
                    app=self,
                )

    def set_game_state(self, state):
        """Set the game state."""
        self.game_state = state

    def unset_timers(self):
        """Unset all the timers."""
        for timer in self.timers.values():
            timer["value"] = None

    def timer_unset(self, timer):
        """Unset this timer."""
        self.timers[timer]["value"] = None

    def timer_active(self, timer):
        """Is thie timer live?"""
        return (
            ticks_ms() - self.timers[timer]["value"] <= self.timers[timer]["duration"]
        )

    def timer_expired(self, timer):
        """Has this timer expired?"""
        if self.timers[timer]["value"]:
            return (
                ticks_ms() - self.timers[timer]["value"]
                > self.timers[timer]["duration"]
            )

        return True

    def set_timer(self, timer):
        """Trigger this timer."""
        self.timers[timer]["value"] = ticks_ms()

    def play_sequence(self):
        """Play the sequence."""
        if self.game_board.inactive():
            if self.sequence_index < len(self.sequence):
                self.game_board[self.sequence[self.sequence_index]].activate()
                self.sequence_index += 1
            else:
                self.set_game_state("GUESS")

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(Background())

        for panel in self.game_board.panels:
            self.overlays.append(panel)

        if self.scoreboard.score < self.score:
            self.scoreboard.score += 1
        self.overlays.append(self.scoreboard)

        self.draw_overlays(ctx)

        if self.dialog:
            self.dialog.draw(ctx)

    def scan_guess_buttons(self):
        """Buttons for Guessing stage."""
        for panel in self.game_board.panels:
            if self.button_states.get(panel.button):
                self.button_states.clear()
                panel.activate()
                self.guessed_sequence.append(panel.index)

    def scan_ready_buttons(self):
        """Buttons for Ready stage."""
        if self.shaken():
            self.button_states.clear()
            self.set_timer("next-round")
            self.set_game_state("NEXT-ROUND")

    def scan_buttons(self):
        """Always scan here."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()


__app_export__ = Simon
