from math import fabs, atan2, cos, degrees, radians
from typing import cast

from PyQt6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QWidget, QStyleOptionGraphicsItem, QGraphicsEllipseItem, QGraphicsScene
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QTransform
from PyQt6.QtCore import QPointF, QRectF, QPoint


class Line(QGraphicsPixmapItem):
    vertex1: QGraphicsItem
    vertex2: QGraphicsItem
    width: float
    height: float
    MAX_WIDTH = 30

    def __init__(self, start: QGraphicsItem, end: QGraphicsItem | QPointF, *args, **kwargs) \
            -> None:
        super().__init__(*args, **kwargs)
        self.vertex1 = start

        if isinstance(end, QGraphicsItem):
            self.vertex2 = end
            self.width = min([self.MAX_WIDTH, start.boundingRect().width(), start.boundingRect().height(),
                              end.boundingRect().width(), end.boundingRect().height()])
        else:
            self.vertex2 = QGraphicsEllipseItem(0, 0, 0, 0)
            self.vertex2.setPos(end)
            self.width = min([self.MAX_WIDTH, start.boundingRect().width(), start.boundingRect().height()])

        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)

        self.setPos(self.vertex1.sceneBoundingRect().center() - QPointF(self.width / 2, 0))

        self.update_pixmap(self.vertex2)

    def setV2(self, end: QGraphicsItem) -> None:
        self.vertex2 = end

    # recalculate height and rotation of pixmap
    def update_pixmap(self, moved_vertex: QGraphicsItem) -> None:
        # simple deduction of static vertex
        moved_point = moved_vertex.sceneBoundingRect().center()
        self.setRotation(0)
        self.setScale(1)

        # moved_vertex is second vertex or ellipse (which means it follows mouse)
        if moved_vertex is self.vertex2 or isinstance(moved_vertex, QGraphicsEllipseItem):
            static_point = self.vertex1.sceneBoundingRect().center()
            if isinstance(moved_vertex, QGraphicsEllipseItem):
               self.vertex2 = moved_vertex
        else:
            static_point = self.vertex2.sceneBoundingRect().center()

        # line will be rotated around its vertices
        self.setTransformOriginPoint(self.mapFromScene(static_point))

        self.setRotation(-1 * degrees(atan2(moved_point.x() - static_point.x(), moved_point.y() - static_point.y())))

        # hypotenuse of right triangle of vertices, rotation is an angle between them
        if self.rotation() == 0:
            self.height = fabs(static_point.y() - moved_point.y())
        else:
            self.height = fabs((static_point.y() - moved_point.y()) / cos(radians(self.rotation())))

        # height is just distance between y's
        self.setPixmap(QPixmap(int(self.width), int(self.height)))

        self.update()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem = None, widget: QWidget = None) -> None:
        painter.save()
        pen = QPen(QColor("blue"), 3)
        painter.setPen(pen)

        # draw straight line in the parallel to y-axis
        painter.drawLine(QPointF(self.width / 2, 0),
                         QPointF(self.width / 2, self.height))

        trcolor = QColor("blue")
        trcolor.setAlphaF(0.5)
        trbrush = QBrush(trcolor)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.setBrush(trbrush)
        painter.drawRect(self.pixmap().rect())

        painter.restore()

    def boundingRect(self) -> QRectF:
        return super(Line, self).boundingRect()
