import weakref

from chi_editor.bases.alpha_atom import AlphaAtom
from chi_editor.bases.molecule.molecule_drawer import MoleculeDrawer


class Molecule:
    atoms: weakref.WeakSet[AlphaAtom]
    molecule_drawer: MoleculeDrawer

    def __init__(self, atom: AlphaAtom) -> None:
        self.atoms = weakref.WeakSet()
        self.atoms.add(atom)
        self.molecule_drawer = MoleculeDrawer(self.atoms)

    def add_atom(self, atom: AlphaAtom) -> None:
        self.atoms.add(atom)

    def remove_atom(self, atom: AlphaAtom) -> None:
        self.atoms.remove(atom)
        if len(self.atoms) == 0:
            self.remove_anchor()

    def remove_anchor(self):
        if self.molecule_drawer.scene() is not None:
            self.molecule_drawer.scene().removeItem(self.molecule_drawer)

    def destroy(self):
        atoms_to_remove: weakref.WeakSet[AlphaAtom] = self.atoms.copy()
        for atom in atoms_to_remove:
            atom.remove()

    def update_atoms(self) -> None:
        queue: list[AlphaAtom] = [atom for atom in self.atoms]
        while queue:
            current_atom: AlphaAtom = queue.pop()
            if current_atom.molecule != self:
                current_atom.molecule.remove_atom(current_atom)
            current_atom.molecule = self
            self.atoms.add(current_atom)
            queue.extend(
                [
                    x
                    for x in current_atom.get_adjacent_atoms()
                    if x not in self.atoms and x not in queue
                ]
            )
        self.molecule_drawer.update_position([atom for atom in self.atoms])
