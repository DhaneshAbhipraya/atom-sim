from atom import Atom
from constraint import Constraint
import pygame as pg
from math import atan2, degrees
from random import randint as r
from threading import Thread


def lerp(a: float, b: float, t: float):
    return ((1 - t) * a) + (t * b)


def main():
    pg.init()
    size = (800, 600)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("atom sim")

    fps = 75
    atoms: list[Atom] = []
    constraints: list[Constraint] = []
    atoms.append(Atom(r=20))
    atoms.append(Atom(r=20))
    constraints.append(Constraint(*atoms))

    # for i in range(100):
    #     newAtom = Atom(pg.Vector2(r(0,size[0]),r(0,size[1])),charge=1.0)
    #     atoms.append(newAtom)

    heldatom: Atom = None  # type: ignore
    steps = 5
    running = True

    clock = pg.time.Clock()

    Thread(target=console).start()
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.MOUSEBUTTONDOWN:
                pass
                # if pg.mouse.get_pressed()[0]:
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    newAtom = Atom(pg.Vector2(pos), 20)
                    # newAtom.apply_force(pg.Vector2(r(-1000,1000),r(-1000,1000)))
                    atoms.append(newAtom)
        if pg.mouse.get_pressed()[1]:
            pos = pg.mouse.get_pos()
            x = [s for s in atoms if s.collidepoint(pos)]
            for i in x:
                atoms.remove(i)

        def m():
            global heldatom
            if pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()
                x = [s for s in atoms if s.collidepoint(pos)]
                if heldatom is None:  # type: ignore
                    if len(x) > 0: heldatom = x[0]
                    return
                f = pg.Vector2(pos)
                heldatom.apply_force((f - heldatom.pos) * 10)  # type: ignore
                heldatom.vel = pg.Vector2()  # type: ignore
                # heldatom.pos=pg.Vector2(pos[0]+r(-1,1),pos[1]+r(-1,1))
                pg.mouse.set_visible(False)
            else:
                pg.mouse.set_visible(True)
                heldatom = None

        Thread(target=m).start()

        # -- gamelogic
        # print(len(atoms))
        for atom in atoms:
            for s in range(steps):
                atom.apply_force(pg.Vector2(0, 9.807))
                orr = atom.r
                while True:
                    for x in atoms:
                        if atom.collideatom(x):
                            i = x
                            break
                    # any([atom.collideatom(x) for x in atoms])
                    # if :
                    #     i=x
                    #     break
                    atom.r += 10
                    break
                atom.r = orr
                collide(atom, i)  # type: ignore

                if atom.pos.y > size[1] - atom.r:
                    atom.pos.y = size[1] - atom.r
                    atom.vel.y *= -wallcr
                if atom.pos.y < atom.r:
                    atom.pos.y = atom.r
                    atom.vel.y *= -wallcr
                if atom.pos.x > size[0] - atom.r:
                    atom.pos.x = size[0] - atom.r
                    atom.vel.x *= -wallcr
                if atom.pos.x < atom.r:
                    atom.pos.x = atom.r
                    atom.vel.x *= -wallcr
                # ua=atom.vel
                # ub=i.vel #type:ignore
                atom.update((fps * steps) / 100)
        atoms.sort()
        for constraint in constraints:
            if not constraint.atom1 in atoms or not constraint.atom2 in atoms:
                constraints.remove(constraint)
            constraint.update()
        # --
        screen.fill((0, 0, 0))

        # -- draw
        for atom in atoms:
            # print((round(255-atom.life),round(255-atom.life),round(255-atom.life)))
            try:
                pg.draw.circle(screen, (255, 255, 255),
                               (atom.pos.x, atom.pos.y), atom.r)
            except ValueError:
                atoms.remove(atom)
        for constraint in constraints:
            pg.draw.line(screen, (255, 255, 255), constraint.atom1.pos,
                         constraint.atom2.pos, 10)
        # --
        pg.display.flip()

        clock.tick(fps)

    pg.quit()


if __name__ == "__main__":
    wallcr = .5
    circcr = .8

    def collide(atom, i):
        if i == atom: return

        center = atom.pos - i.pos
        angle = atan2(center.y, center.x)
        vangle = pg.Vector2()
        vangle.from_polar((1, degrees(angle)))
        # atom.vel=atom.vel.reflect(vangle)
        # i.vel=i.vel.reflect(vangle)
        # print(angle)
        # print(vangle)
        atom.vel, i.vel = [x.vel.reflect(vangle) for x in [atom, i]]
        atom.pos = atom.pos + vangle
        i.pos = i.pos - vangle
        # try:
        #     cr=max(min((atom.vel*i.vel)/(ua*ub),1),0)
        # except ZeroDivisionError:pass
        cr = circcr
        atom.vel, i.vel = [x.vel * cr for x in [atom, i]]

    def console():
        global circcr, wallcr, atoms
        while True:
            try:
                cmd = input("> ")
            except EOFError:
                pg.quit()
                quit()
            try:
                print(eval(cmd))
            except SyntaxError:
                pass
            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    main()
