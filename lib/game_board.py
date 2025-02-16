from .conf import conf
from .panel import Panel


class GameBoard:
    """A board for games."""

    def __init__(self):
        """Construct."""
        self.panels = [Panel(item) for item in conf["panels"]]

    def inactive(self):
        """Are all our panels inactive?"""
        return all(panel.ready for panel in self.panels)

    def __getitem__(self, index):
        """Get a panel."""
        return self.panels[index]
