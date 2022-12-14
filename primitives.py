from pygame import Vector2
from atom import Atom
from constraint import Constraint


def line(length: int,
         atomseq: list[Atom],
         constraintseq: list[Constraint],
         s: int = 10,
         x: int = 0,
         y: int = 0) -> None:
    prevAtom = None
    for i in range(x, x + length * (s * 2), s * 2):
        newAtom = Atom(Vector2(i, y), s)
        atomseq.append(newAtom)
        if prevAtom is not None:
            constraintseq.append(Constraint(prevAtom, newAtom, 5))
        prevAtom = newAtom
