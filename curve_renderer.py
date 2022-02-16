from ursina import *

'''
Renders a Bezier curve based on given points.
'''

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

    def set_curve(self, points):
        curve_points = [self.mlerp(points, i / (self.length - 1)) for i in range(self.length)]

        dir = (curve_points[1] - curve_points[0]).normalized()
        dir = self.swapxy(dir) * self.thickness * 0.5
        self.renderer.model.vertices[0:2] = [curve_points[0] + dir, curve_points[0] - dir]

        dir = (curve_points[-2] - curve_points[-1]).normalized()
        dir = self.swapxy(dir) * self.thickness * 0.5
        self.renderer.model.vertices[-1:-3:-1] = [curve_points[-1] + dir, curve_points[-1] - dir]
        
        for i in range(1, self.length - 1):
            dir = ((curve_points[i + 1] - curve_points[i]).normalized() + (curve_points[i] - curve_points[i - 1]).normalized()).normalized()
            dir = self.swapxy(dir) * self.thickness * 0.5

            self.renderer.model.vertices[i*2  ] = curve_points[i] + dir
            self.renderer.model.vertices[i*2+1] = curve_points[i] - dir

        self.renderer.model.generate()

    def mlerp(self, points, t):
        if abs(t) < 0.000001: return points[0]
        if abs(t - 1) < 0.000001: return points[-1]
        # if len(points) > 3: return self.mlerp([points[0], self.mlerp(points[1:-1], t), points[-1]], t)
        ps = copy(points)
        for i in range(len(ps) - 1, 0, -1):
            for j in range(i):
                ps[j] = ps[j] + (ps[j+1] - ps[j]) * t         
        return ps[0]