from ursina import *
from Prefabs.instanced_entity import InstancedEntity, InstancedGroup
from ExtraData.builtin_shaders import Instanced_Curve_Shader

class InstancedCurve(InstancedEntity):

    main_group:InstancedGroup = None

    def __init__(self, **kwargs):
        self.relative_position = Vec4(0,0,0,0)
        self.c_val1 = [0,0, 0,0]
        self.c_val2 = [0,0, 0,0]

        super().__init__(**( {'parent' : camera.ui} | kwargs | {'collider' : None}))
    
    def visible_test(self):
        e = self
        while e != None:
            if not hasattr(e, 'visible'): return True
            if not e.visible or not e.enabled: return False
            e = e.parent
        return True

    def __setattr__(self, name, value):
        if name == 'visible' and self.instance_group != None:
            self.instance_group.update_value(self, 'color', self.color if value else (0,0,0,0))
        return super().__setattr__(name, value)

    def set_curve(self, points):
        points = [Vec2(p[0], p[1]) for p in points]
        if len(points) == 2:
            points = [points[0], lerp(points[0], points[1], 0.3), lerp(points[0], points[1], 0.7), points[1]]

        a = (points[1] - points[0])*3
        b = (points[2] - points[1])*3
        c = (points[3] - b - points[0])
        b -= a
        # self.c_val = [c, b, a, points[0]]
        self.c_val1 = [c.x, c.y, b.x, b.y]
        self.c_val2 = [a.x, a.y, points[0].x, points[0].y]

        if self.instance_group != None:
            np = self.get_position(self.instance_group)
            if self.relative_position.xyz != np:
                self.relative_position = Vec4(np, 0)

    def init_group(parent):
        length = 100
            
        InstancedCurve.main_group = InstancedGroup(
            parent = parent,
            default_class = InstancedCurve,
            model = Mesh(vertices = [(floor(i/2) / (length - 1),  ((i + 1)%2) - 0.5, 0) for i in range(length * 2)], mode='tristrip', static=False),
            shader_attributes = {
                'relative_position' : 'positions' ,
                'c_val1' : 'Cvals1',
                'c_val2' : 'Cvals2',
                'color' : 'colors'
            }, 
            max_count = 128,
            shader = Shader(vertex = Instanced_Curve_Shader['vertex'], fragment = Instanced_Curve_Shader['fragment'])
            )
        InstancedCurve.main_group.set_shader_input('thickness', 0.005)

    def update_visibility():
        p = InstancedCurve.main_group
        while p != None:
            for e in p.entities:
                e.instance_group.update_value(e, 'color', e.color if e.visible_test() else (0,0,0,0))
            p = p.group_chain


if __name__ == '__main__':
    app = Ursina(vsync = False)

    InstancedCurve.init_group(camera.ui)

    e = InstancedCurve.main_group.new_entity(parent = camera.ui, color = color.green, position = Vec3(0,0,-0))
    e2 = InstancedCurve.main_group.new_entity(parent = camera.ui, color = color.green, position = Vec3(0,0,-0))
    e.set_curve([(0,0), (0.1,0), (0.1,0.1), (0.2,0.1)])
    e2.set_curve([(0,0), (-0.1,0), (-0.1,0.1), (0,0.1)])

    for i in range(300):
        e3 = InstancedCurve.main_group.new_entity(parent = camera.ui, color = color.hsv(random.uniform(0,360), 0.5, 0.5,1), position = Vec3(0,0,-0))
        e3.set_curve([(random.uniform(-1,1),random.uniform(-1,1)), (random.uniform(-1,1),random.uniform(-1,1)), (random.uniform(-1,1),random.uniform(-1,1)), (random.uniform(-1,1),random.uniform(-1,1))])

    app.run()