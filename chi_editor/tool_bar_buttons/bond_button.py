from tool_bar_buttons.toolbar_button import ToolBarButton


class BondButton(ToolBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Bond")
