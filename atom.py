from math import dist
from typing import Any
from pygame import Vector2


class Atom:
    def __init__(self,
                 pos: Vector2 = Vector2(0, 0),
                 r: float = 10,
                 static: bool = False,
                 **custom_props: Any) -> None:
        self.pos = pos
        self.vel = Vector2()
        self.acc = Vector2()
        self.r = r
        self.m = r
        self.static = static
        self.custom_props = custom_props
        self.life: float = 0.0

    def update(self, fps: float):
        self.vel += self.acc / fps
        if not self.static: self.pos += self.vel / fps
        self.acc = Vector2()
        self.life += 1 / fps

    def apply_force(self, force: Vector2):
        self.acc += force / self.m

    def collidepoint(self, point: tuple):
        return point[0] > self.pos.x - self.r and point[
            0] < self.pos.x + self.r and point[
                1] > self.pos.y - self.r and point[1] < self.pos.y + self.r

    def distanceto(self, atom: 'Atom', radius: bool = True):
        return dist(
            self.pos,  #type:ignore
            atom.pos) - (self.r + atom.r) * radius  #type:ignore

    def collideatom(self, atom: 'Atom'):
        return self.distanceto(atom) < 0

    def __lt__(self, other):
        return other.life < self.life


class StaticAtom(Atom):
    def __init__(self,
                 pos: Vector2 = Vector2(0, 0),
                 r: float = 10,
                 **custom_props: Any) -> None:
        super().__init__(pos, r, True, **custom_props)
