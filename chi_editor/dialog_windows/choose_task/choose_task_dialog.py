from typing import TYPE_CHECKING, cast
from random import randint

from PyQt6.QtWidgets import QDialog, QTreeView, QSizePolicy, QVBoxLayout, QAbstractItemView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QModelIndex

from chi_editor.api.task import Task, Kind

from chi_editor.editor_mode import EditorMode

if TYPE_CHECKING:
    from chi_editor.editor import Editor


class ChooseTaskDialog(QDialog):
    # Main window
    editor: "Editor"

    # View that holds all the tasks links
    view: QTreeView

    # Layout that holds view to make it expandable
    layout: QVBoxLayout

    # Model that links to all the tasks
    model: QStandardItemModel

    # Mapping from kinds to their entries in model
    kind_items: dict[Kind, QStandardItem]

    def __init__(self, *args, editor: "Editor", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Choose a task")

        self.editor = editor

        # Model init
        self.model = QStandardItemModel()
        self.kind_items = {}

        # View init
        self.view = QTreeView(self)
        self.view.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.handleDoubleClick)
        self.view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.view.setHeaderHidden(True)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 2, 0, 0)
        self.layout.addWidget(self.view)

    def updateKindsDict(self, kind: Kind) -> None:
        kind_item = QStandardItem(kind.name)
        kind_item.setData(kind, Qt.ItemDataRole.UserRole)
        self.model.appendRow(kind_item)
        self.kind_items.update({kind: kind_item})

    def addTask(self, task: Task):
        task_item = QStandardItem(task.name)
        task_item.setData(task, Qt.ItemDataRole.UserRole)

        if task.kind not in self.kind_items:
            self.updateKindsDict(task.kind)

        kind_item = self.kind_items.get(task.kind)  # get item containing corresponding kind with dictionary
        kind_item.appendRow(task_item)

    def _clearTasksList(self) -> None:
        for r in range(0, self.model.rowCount()):  # run through top level categories and remove their contents (rows)
            kind_row = self.model.item(r)
            kind_row.removeRows(0, kind_row.rowCount())

    def handleAcceptClick(self):
        self.handleDoubleClick(self.view.currentIndex())

    def handleDoubleClick(self, index: QModelIndex) -> None:
        task_item = self.model.itemFromIndex(index)
        task = task_item.data(Qt.ItemDataRole.UserRole)
        if isinstance(task, Task):
            self.chooseTask(task)

    def chooseTask(self, task: Task) -> None:
        self.editor.setMode(EditorMode.SOLVE_MODE)
        self.editor.setTask(task=task)
        self.close()

    def handleDeleteClick(self, index: Task) -> None:
        pass

    def handleRandomTaskClick(self) -> None:
        type_id: int = randint(0, self.model.rowCount() - 1)
        type_item = self.model.itemFromIndex(self.model.index(type_id, 0))

        task_id = randint(0, type_item.rowCount() - 1)
        task_item = type_item.child(task_id, 0)
        self.chooseTask(task_item.data(Qt.ItemDataRole.UserRole))

    def loadTasks(self) -> None:
        pass
