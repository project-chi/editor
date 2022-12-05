import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QButtonGroup

from .new_canvas import Canvas
from .menu_bar import MenuBar
from .toolbar import create_toolbar
from .experiment_ui import Ui_Dialog


class Editor(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.menu_bar = MenuBar()
        self.tool_bar = create_toolbar()

        self.setupUi(self)
        self.scene = Canvas(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        group = QButtonGroup(self)
        group.addButton(self.radioButton)
        group.addButton(self.radioButton_2)

        group.buttonClicked.connect(lambda btn: self.scene.setOption(btn.text()))
        self.radioButton.setChecked(True)
        self.scene.setOption(self.radioButton.text())

        self.setWindowTitle("Project Chi")
        # to be changed to relative dimensions or whatever
        self.resize(400, 200)
        self.setWindowIcon(QIcon("..\\resources\\ProjectChi.png"))
        self.setMenuBar(self.menu_bar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.tool_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Editor()
    win.show()
    sys.exit(app.exec())
