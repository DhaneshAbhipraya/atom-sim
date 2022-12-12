from math import atan2
from atom import Atom
from typing import Any
from pygame import Vector2


class Constraint:
    def __init__(self, atom1: Atom, atom2: Atom) -> None:
        self.atom1 = atom1
        self.atom2 = atom2

    def update(self):
        atom1angle = self.atom1.pos.angle_to(self.atom2.pos)
        atom2angle = self.atom2.pos.angle_to(self.atom1.pos)
        x = Vector2()
        x.from_polar((1, atom1angle))
        x = x + (self.atom2.pos - self.atom1.pos)
        self.atom1.apply_force(x)  # type: ignore
        y = Vector2()
        y.from_polar((1, atom2angle))
        y = y + (self.atom1.pos - self.atom2.pos)
        self.atom2.apply_force(y)  # type: ignore
