import math
import numpy as np


class Vector:
    def __init__(self, *,
                 px: float = None, py: float = None, pz: float = None, w: float = None,
                 ax: float = None, by: float = None, cz: float = None,
                 ):
        if self.type_a_check(px, py, pz, w, ax, by, cz):
            self.px = px
            self.py = py
            self.pz = pz
            self.w = w

            self.ax = px / w
            self.by = py / w
            self.cz = pz / w

        elif self.type_b_check(px, py, pz, w, ax, by, cz):
            self.ax = ax
            self.by = by
            self.cz = cz

            if w is None:
                w = 1

            self.px = self.ax * w
            self.py = self.by * w
            self.pz = self.cz * w
        else:
            raise ValueError("Not all necessary values informed")

        self._npvec = np.array([self.ax, self.by, self.cz])

        self._changed = True
        self._unitary = None
        self._module = None

        self.is_unitary()
        self.norm()

    def __add__(self, other):
        if type(other) == Vector:
            return Vector(
                px=self.px + other.px,
                py=self.py + other.py,
                pz=self.pz + other.pz,
                w=self.w + other.w,
            )
        else:
            raise ValueError(f"Cannot sum {Vector} with {type(other)}")

    def __str__(self):
        return (
            f"Vector\n"
            f"px = {self.px}\n"
            f"py = {self.py}\n"
            f"pz = {self.pz}\n"
            f"w  = {self.w}\n"
            f"ax = {self.ax}\n"
            f"by = {self.by}\n"
            f"cz = {self.cz}\n"
        )

    def _change_f(self):
        if self._changed is True:
            self.is_unitary()
            self.norm()

            self._changed = False

    def is_unitary(self):
        if self._changed:
            if np.linalg.norm(self._npvec) == 1:
                self._unitary = True
        return self._unitary

    def norm(self):
        if self._changed:
            self._module = math.sqrt(pow(self.ax, 2) + pow(self.by, 2) + pow(self.cz, 2))
        return self._module

    @staticmethod
    def type_a_check(px, py, pz, w, ax, by, cz):
        return px is not None and \
               py is not None and \
               pz is not None and \
               w is not None and \
               ax is None and \
               by is None and \
               cz is None

    @staticmethod
    def type_b_check(px, py, pz, w, ax, by, cz):
        return px is None and \
               py is None and \
               pz is None and \
               ax is not None and \
               by is not None and \
               cz is not None


class RobMatrix:
    def __init__(self,
                 nx: float, ox: float, ax: float, px: float,
                 ny: float, oy: float, ay: float, py: float,
                 nz: float, oz: float, az: float, pz: float,
                 w: float
                 ):
        self._matrix_keys = [
            "nx", "ox", "ax", "px",
            "ny", "oy", "ay", "py",
            "nz", "oz", "az", "pz",
            "w"
        ]
        self.matrix = {
            "nx": nx, "ox": ox, "ax": ax, "px": px,
            "ny": ny, "oy": oy, "ay": ay, "py": py,
            "nz": nz, "oz": oz, "az": az, "pz": pz,
            "w": w
        }
        self.nx = nx
        self.ox = ox
        self.ax = ax
        self.px = px
        self.ny = ny
        self.oy = oy
        self.ay = ay
        self.py = py
        self.nz = nz
        self.oz = oz
        self.az = az
        self.pz = pz
        self.w = w

        self._rotationdict = {
            'x': self._rotx,
            'y': self._roty,
            'z': self._rotz,
            'n': self._rotx,
            'o': self._roty,
            'a': self._rotz,
        }

    def __str__(self):
        s = (f"___________________________\n"
             f"| {self.matrix.get('nx'):.2f}{' ' if self.matrix.get('nx') >= 0 else ''}"
             f"  {self.matrix.get('ox'):.2f}{' ' if self.matrix.get('ox') >= 0 else ''}"
             f"  {self.matrix.get('ax'):.2f}{' ' if self.matrix.get('ax') >= 0 else ''}"
             f"  {self.matrix.get('px'):.2f}{' ' if self.matrix.get('px') >= 0 else ''} |\n"
             f"| {self.matrix.get('ny'):.2f}{' ' if self.matrix.get('ny') >= 0 else ''}"
             f"  {self.matrix.get('oy'):.2f}{' ' if self.matrix.get('oy') >= 0 else ''}"
             f"  {self.matrix.get('ay'):.2f}{' ' if self.matrix.get('ay') >= 0 else ''}"
             f"  {self.matrix.get('py'):.2f}{' ' if self.matrix.get('py') >= 0 else ''} |\n"
             f"| {self.matrix.get('nz'):.2f}{' ' if self.matrix.get('nz') >= 0 else ''}"
             f"  {self.matrix.get('oz'):.2f}{' ' if self.matrix.get('oz') >= 0 else ''}"
             f"  {self.matrix.get('az'):.2f}{' ' if self.matrix.get('az') >= 0 else ''}"
             f"  {self.matrix.get('pz'):.2f}{' ' if self.matrix.get('pz') >= 0 else ''} |\n"
             f"| 0      0      0      {self.matrix.get('w'):.2f}{' ' if self.matrix.get('w') >= 0 else ''} |\n"
             f"‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        return s

    def __mul__(self, other):
        if type(self) != type(other):
            raise TypeError(f'cant multiply if type is nor {type(self)}')
        return self._multiply(other)

    def _multiply(self, other):
        other: RobMatrix

        return RobMatrix(
            nx=self.nx * other.nx + other.ny * self.ox + self.ax * other.nz,
            ox=other.oy * self.ox + self.nx * other.ox + self.ax * other.oz,
            ax=other.az * self.ax + other.ax * self.nx + other.ay * self.ox,
            px=other.w * self.px + self.nx * other.px + self.ax * other.pz + other.py * self.ox,
            ny=self.ny * other.nx + other.ny * self.oy + self.ay * other.nz,
            oy=self.oy * other.oy + self.ny * other.ox + self.ay * other.oz,
            ay=other.az * self.ay + self.ny * other.ax + other.ay * self.oy,
            py=self.py * other.w + self.ny * other.px + other.py * self.oy + self.ay * other.pz,
            nz=other.ny * self.oz + other.nx * self.nz + self.az * other.nz,
            oz=other.oy * self.oz + self.az * other.oz + other.ox * self.nz,
            az=self.az * other.az + other.ay * self.oz + other.ax * self.nz,
            pz=other.w * self.pz + self.az * other.pz + other.py * self.oz + other.px * self.nz,
            w=self.w * other.w,
        )

    def det(self):
        pass

    def inverse(self):
        return RobMatrix(
            nx=self.nx,
            ox=self.ny,
            ax=self.nz,
            px=-(self.px * self.nx + self.py * self.ny + self.pz * self.nz),

            ny=self.ox,
            oy=self.oy,
            ay=self.oz,
            py=-(self.px * self.ox + self.py * self.oy + self.pz * self.oz),

            nz=self.ax,
            oz=self.ay,
            az=self.az,
            pz=-(self.px * self.ax + self.py * self.ay + self.pz * self.az),

            w=self.matrix.get("w")
        )

    def trans(self, axis, dx, dy, dz):
        if axis in ['x', 'y', 'z']:
            mult = 'pre'
        elif axis in ['n', 'o', 'a']:
            mult = 'post'
        else:
            raise ValueError('type must be one of: x y z n o a')
        trans = RobMatrix(
            nx=1,
            ox=0,
            ax=0,
            px=dx,
            ny=0,
            oy=1,
            ay=0,
            py=dy,
            nz=0,
            oz=0,
            az=1,
            pz=dz,
            w=1,
        )

        if mult == 'pre':
            return trans * self
        else:
            return self * trans

    def rot(self, axis, teta: float):
        if axis in ['x', 'y', 'z']:
            mult = 'pre'
        elif axis in ['n', 'o', 'a']:
            mult = 'post'
        else:
            raise ValueError('type must be one of: x y z n o a')

        if mult == 'pre':
            return self._rotationdict[axis](teta) * self
        else:
            return self * self._rotationdict[axis](teta)

    def _rotx(self, teta: float):
        return RobMatrix(**{
            "nx": 1, "ox": 0, "ax": 0, "px": 0,
            "ny": 0, "oy": math.cos(teta), "ay": -math.sin(teta), "py": 0,
            "nz": 0, "oz": math.sin(teta), "az": math.cos(teta), "pz": 0,
            "w": 1
        })

    def _roty(self, teta: float):
        return RobMatrix(**{
            "nx": math.cos(teta), "ox": 0, "ax": math.sin(teta), "px": 0,
            "ny": 0, "oy": 1, "ay": 0, "py": 0,
            "nz": -math.sin(teta), "oz": 0, "az": math.cos(teta), "pz": 0,
            "w": 1
        })

    def _rotz(self, teta: float):
        return RobMatrix(**{
            "nx": math.cos(teta), "ox": -math.sin(teta), "ax": 0, "px": 0,
            "ny": math.sin(teta), "oy": math.cos(teta), "ay": 0, "py": 0,
            "nz": 0, "oz": 0, "az": 1, "pz": 0,
            "w": 1
        })
