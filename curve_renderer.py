from ursina import *

class CurveRenderer(Entity):
    '''
    def __init__(self, thickness=10, length=15, **kwargs):
        super().__init__(**kwargs)
        self.renderer = Entity(
            parent = self,
            model = Mesh(
            vertices=[self.world_position for i in range(length)],
            mode='line',
            thickness=thickness,
            static=False
            )
        )
        self.renderer.color = color.white

    

    def set_curve(self, points):
        count = len(self.renderer.model.vertices)
        for i in range(count):
            self.renderer.model.vertices[i] = self.mlerp(points, i / (count - 1))
        self.renderer.model.generate()
    '''

    def __init__(self, thickness=0.005, length=25, color=color.white, **kwargs):
        super().__init__(**kwargs)
        self.renderer = Entity(
            parent = self,
            model = Mesh(
            vertices=[self.world_position for i in range(length * 2)],
            mode='tristrip',
            static=False
            )
        )
        self.renderer.color = color
        self.thickness = thickness
        self.length = length

        for key, value in kwargs.items():
            setattr(self, key, value)

    
    def swapxy(self, p):
        p.x, p.y = -p.y, p.x
        return p

    def magnitude(self, p):
        from math import sqrt 
        return sqrt(sum(p[i] ** 2 for i in range(len(p))))

    def normalize(self, p):
        m = self.magnitude(p)
        if m < 0.00000001:
            return Vec3(0,0,0)
        for i in range(len(p)):
            p[i] /= m
        return p

    def set_curve(self, points):
        curve_points = [self.mlerp(points, i / (self.length - 1)) for i in range(self.length)]

        dir = self.normalize(curve_points[1] - curve_points[0])
        dir = self.swapxy(dir) * self.thickness * 0.5
        self.renderer.model.vertices[0:2] = [curve_points[0] + dir, curve_points[0] - dir]

        dir = self.normalize(curve_points[-2] - curve_points[-1])
        dir = self.swapxy(dir) * self.thickness * 0.5
        self.renderer.model.vertices[-1:-3:-1] = [curve_points[-1] + dir, curve_points[-1] - dir]
        
        for i in range(1, self.length - 1):
            dir = self.normalize(self.normalize(curve_points[i + 1] - curve_points[i]) + self.normalize(curve_points[i] - curve_points[i - 1]))
            dir = self.swapxy(dir) * self.thickness * 0.5

            self.renderer.model.vertices[i*2  ] = curve_points[i] + dir
            self.renderer.model.vertices[i*2+1] = curve_points[i] - dir

        self.renderer.model.generate()

    def mlerp(self, points, t):
        ps = copy(points)
        while len(ps) > 1:
            ps = [lerp(ps[j], ps[j+1], t) for j in range(len(ps) - 1)]            
        return ps[0]

    def on_destroy(self):
        destroy(self.renderer)