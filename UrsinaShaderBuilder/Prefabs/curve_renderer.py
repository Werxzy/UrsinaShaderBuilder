from ursina import *
from ExtraData.builtin_shaders import Curve_Shader
from panda3d.core import BoundingBox

'''
Renders a Bezier curve based on given points.
'''

class CurveRenderer(Entity):

    meshes:dict[int, list[tuple[float, float, float]]] = {}
    
    def __init__(self, thickness=0.005, length=25, color=color.white, **kwargs):
        super().__init__(**kwargs)
        shader = Shader(vertex = Curve_Shader['vertex'], fragment = Curve_Shader['fragment'])

        if length not in CurveRenderer.meshes:
            CurveRenderer.meshes.update({length : [(floor(i/2) / (length - 1),  ((i + 1)%2) - 0.5, 0) for i in range(length * 2)] })
        
        self.renderer = Entity(
            parent = self,
            model = Mesh(vertices = CurveRenderer.meshes[length], mode='tristrip', static=False),
            shader = shader
        )
        
        self.set_shader_input('thickness', thickness)
        self.set_shader_input('C1', (0,0))
        self.set_shader_input('C2', (0,0))
        self.set_shader_input('C3', (0,0))
        self.set_shader_input('C4', (0,0))

        self.renderer.color = color
        self.length = length

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_curve(self, points):
        points = [Vec2(p.x, p.y) for p in points]
        if len(points) == 2:
            points = [points[0], lerp(points[0], points[1], 0.3), lerp(points[0], points[1], 0.7), points[1]]

        a = (points[1] - points[0])*3
        b = (points[2] - points[1])*3
        c = (points[3] - b - points[0])
        b -= a

        self.set_shader_input('C1', c)
        self.set_shader_input('C2', b)
        self.set_shader_input('C3', a)
        self.set_shader_input('C4', points[0])

        mins = Vec3(points[0].x, points[0].y, 0)
        maxs = Vec3(points[0].x, points[0].y, 0)
        for p in points:
            for x in range(2):
                mins[x] = min(mins[x], p[x])
                maxs[x] = max(maxs[x], p[x])

        node = self.node()
        node.setBounds(BoundingBox(mins, maxs))
        node.setFinal(True)