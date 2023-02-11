from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent

from ...bases.tool import Tool


class Eraser(Tool):
    def mouse_press_event(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            items = self.canvas.items(event.scenePos(), Qt.ItemSelectionMode.IntersectsItemShape)
            if not items:
                return super(Eraser, self).mouse_press_event(event)
            self.canvas.removeItem(items[0])
        else:
            self.canvas.clear()


    @property
    def asset(self) -> str:
        return 'eraser'
