from enum import Enum

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QIcon, QTransform
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QPushButton, QVBoxLayout, QWidget, QLayout

from .canvas import Canvas
from .constants import ASSETS
from .toolbar import CanvasToolBar


class Editor(QMainWindow):
    class EditorMode(Enum):
        FREE_MODE = 0,
        SOLVE_MODE = 1,
        CREATE_MODE = 2

    # Hierarchy:
    #
    #   window:
    #       workspace:
    #           graphics_view:
    #               canvas:
    #       toolbar:

    # Contains everything except toolbar
    workspace: QWidget

    # QGraphicsView contains drawable space
    graphics_view: QGraphicsView

    # GraphicsScene where to draw all graphical objects
    canvas: Canvas

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window settings
        self.setWindowTitle("Project Chi")
        self.setWindowIcon(QIcon(str(ASSETS / 'project-chi.png')))
        self.resize(1000, 600)

        # The biggest part of interface
        self.workspace = QWidget()  # create workspace
        self.setCentralWidget(self.workspace)

        self.workspace.setLayout(self.getLayout(Editor.EditorMode.FREE_MODE))

        # Add left toolbar
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, CanvasToolBar(canvas=self.canvas))

    def zoom_in(self):
        # Get the current scale factor of the view
        current_scale = self.graphics_view.transform().m11()

        # Update the scale factor of the view
        new_scale = current_scale * 1.2
        self.graphics_view.setTransform(QTransform.fromScale(new_scale, new_scale))

    def zoom_out(self):
        # Get the current scale factor of the view
        current_scale = self.graphics_view.transform().m11()

        # Update the scale factor of the view
        new_scale = current_scale / 1.2
        self.graphics_view.setTransform(QTransform.fromScale(new_scale, new_scale))

        # Add left toolbar
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, CanvasToolBar(canvas=self.canvas))

    def getLayout(self, mode: EditorMode) -> QLayout:
        match mode:
            case Editor.EditorMode.FREE_MODE:
                return self.getFreeModeLayout()
            case Editor.EditorMode.SOLVE_MODE:
                pass
            case Editor.EditorMode.CREATE_MODE:
                pass

    def getFreeModeLayout(self) -> QLayout:
        # Initialize QGraphicsView
        self.graphics_view = QGraphicsView(self)  # create QGraphicsView
        self.graphics_view \
            .setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # Set QGraphicsView position
        self.graphics_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        # Initialize GGraphicsScene called canvas
        self.canvas = Canvas(QRectF(self.graphics_view.geometry()))

        # Bind GraphicsScene to GraphicsView
        self.graphics_view.setScene(self.canvas)

        # Box contains magnifying glass
        v_button_group = QVBoxLayout(self)
        v_button_group.addStretch(1)
        v_button_group.setAlignment(Qt.AlignmentFlag.AlignRight)

        scale_plus = QPushButton("Zoom In", self)
        scale_plus.clicked.connect(self.zoom_in)

        scale_minus = QPushButton("Zoom Out", self)
        scale_minus.clicked.connect(self.zoom_out)

        v_button_group.addWidget(scale_minus)
        v_button_group.addWidget(scale_plus)
        v_button_group.addStretch(1)

        self.graphics_view.setLayout(v_button_group)

        layout = QVBoxLayout(self)
        layout.addWidget(self.graphics_view)
        return layout
   