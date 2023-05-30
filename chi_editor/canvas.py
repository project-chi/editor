from typing import TYPE_CHECKING, overload

from PyQt6.QtCore import QRectF, pyqtSignal
from PyQt6.QtWidgets import QGraphicsScene
from rdkit import Chem

from chi_editor.bases.alpha_atom import AlphaAtom
from chi_editor.bases.molecule import Molecule
from chi_editor.chains.chain import Chain
from chi_editor.chem_utils import mol_from_graphs
from chi_editor.reactions.reaction import Reaction

if TYPE_CHECKING:
    from chi_editor.bases.tool import Tool

    from PyQt6.QtWidgets import QGraphicsSceneMouseEvent


class Canvas(QGraphicsScene):
    current_action: "Tool" = None
    min_scene_rect: "QRectF"
    canvas_in_focus: pyqtSignal = pyqtSignal()

    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)
        self.min_scene_rect = super().sceneRect()

    def add_left_drawing_space(self):
        #TODO
        pass

    def add_right_drawing_space(self):
        #TODO
        pass

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> "None":
        self.canvas_in_focus.emit()
        if self.current_action is not None:
            self.current_action.mouse_press_event(event)

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent") -> "None":
        if self.current_action is not None:
            self.current_action.mouse_move_event(event)

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> "None":
        if self.current_action is not None:
            self.current_action.mouse_release_event(event)

    def enlargeScene(self, sceneRect: "QRectF") -> "None":
        self.min_scene_rect = self.min_scene_rect.united(sceneRect)

    def sceneRect(self) -> "QRectF":
        return self.min_scene_rect

    @overload
    def setSceneRect(self, sceneRect: "QRectF") -> "None":
        ...

    @overload
    def setSceneRect(self, x: "float", y: "float", w: "float", h: "float") -> "None":
        ...

    def setSceneRect(self, *args) -> "None":
        match args:
            case [QRectF() as sceneRect]:
                self.enlargeScene(sceneRect)
            case [float() as x, float() as y, float() as w, float() as h]:
                self.enlargeScene(QRectF(x, y, w, h))
            case _:
                raise TypeError("wrong signature")

    def findMolecule(self):
        items = self.items()
        if len(items) == 0:
            return ""
        molecule: type | None = None
        for item in items:
            if isinstance(item, AlphaAtom):
                molecule = item.molecule
                break
        if molecule is None:
            return ""
        return Chem.MolToSmiles(mol_from_graphs(molecule))

    def findElement(self, element_type: Chain | Reaction):
        items = self.items()
        if len(items) == 0:
            return ""
        element: type | None = None
        for item in items:
            if isinstance(item, element_type):
                element = item
                break
        if element is None:
            return ""
        return element.to_string()

    def more_than_one_molecule(self) -> bool:
        atoms = len(list(filter(lambda item: isinstance(item, AlphaAtom), self.items())))
        if atoms == 0:
            return False
        return atoms > next(filter(lambda item: isinstance(item, AlphaAtom), self.items())).molecule.number_atoms()

    def no_atoms(self) -> bool:
        return len(list(filter(lambda item: isinstance(item, AlphaAtom), self.items()))) == 0
