from typing import TYPE_CHECKING

from PyQt6.QtGui import QActionGroup
from PyQt6.QtWidgets import QToolBar

from chi_editor.toolbar.tools import tools
from PyQt6.QtGui import QAction

if TYPE_CHECKING:
    from chi_editor.canvas import Canvas


class GeneralToolBar(QToolBar):
    _canvas: "Canvas"
    _action_group: "QActionGroup"

    def __init__(self, *args, canvas: "Canvas", **kwargs) -> "None":
        super().__init__(*args, **kwargs)
        self._canvas = canvas
        self.setStyleSheet("""QToolBar { background-color: rgb(212, 204, 234); }""")
        self.setMovable(False)

        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(True)

        for Tool in tools:
            tool = Tool(canvas)
            self.addAction(tool)
            self.action_group.addAction(tool)
            self.widgetForAction(tool).setStyleSheet("padding: 5px")

        self.actionTriggered.connect(self.changeAction)

    def changeAction(self, action: "QAction") -> "None":
        self._canvas.current_action = action

    def change_canvas(self, canvas: "Canvas"):
        self._canvas = canvas
        for Action in self.actions():
            Action.change_canvas(canvas)