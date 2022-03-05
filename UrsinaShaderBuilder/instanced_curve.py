from ursina import *
from Prefabs.instanced_entity import InstancedEntity, InstancedGroup

Instanced_Curve_Shader = {
    "vertex": "#version 450\n\nuniform vec4[128] Cvals1;\nin vec4 p3d_Vertex;\nuniform vec4[128] Cvals2;\nuniform float thickness;\nuniform vec4[128] positions;\nuniform vec4[128] colors;\nuniform mat4 p3d_ModelViewProjectionMatrix;\nin vec2 p3d_MultiTexCoord0;\nout vec4 col;\nout vec2 uv;\nout vec4 gl_Position;\n\nvoid main(){\nvec4[128] _vec4_array_128_3 = colors;\nvec4[128] _vec4_array_128_2 = positions;\nvec4[128] _vec4_array_128_1 = Cvals2;\nvec4[128] _vec4_array_128_0 = Cvals1;\nvec4 _vec4_0 = _vec4_array_128_0[gl_InstanceID];\nvec2 _vec2_0 = vec2(_vec4_0.xy);\nfloat _float_0 = _vec4_0.z;\nfloat _float_1 = _vec4_0.w;\nvec2 _vec2_1 = vec2(_float_0,_float_1);\n_float_1 = p3d_Vertex.x;\n_float_0 = p3d_Vertex.y;\nvec2 _vec2_2=3.0*_vec2_0;\nvec2 _vec2_3=2.0*_vec2_1;\n_vec2_2=_vec2_2*_float_1;\n_vec4_0 = _vec4_array_128_1[gl_InstanceID];\n_vec2_3=_vec2_2+_vec2_3;\n_vec2_2 = vec2(_vec4_0.xy);\nfloat _float_2 = _vec4_0.z;\nfloat _float_3 = _vec4_0.w;\n_vec2_3=_vec2_3*_float_1;\n_vec2_0=_float_1*_vec2_0;\n_vec2_3=_vec2_3+_vec2_2;\n_vec2_1=_vec2_0+_vec2_1;\nfloat _float_4 = _vec2_3.x;\nfloat _float_5 = _vec2_3.y;\n_vec2_1=_float_1*_vec2_1;\n_float_5=_float_5*-1;\n_vec2_2=_vec2_1+_vec2_2;\n_vec2_1 = vec2(_float_5,_float_4);\n_vec2_3 = vec2(_float_2,_float_3);\n_vec2_2=_float_1*_vec2_2;\n_float_0=_float_0*thickness;\n_vec2_1=normalize(_vec2_1);\n_vec2_3=_vec2_2+_vec2_3;\n_vec2_1=_vec2_1*_float_0;\n_vec2_3=_vec2_1+_vec2_3;\n_vec4_0 = vec4(_vec2_3,0,1);\nvec4 _vec4_1 = _vec4_array_128_2[gl_InstanceID];\n_vec4_0=_vec4_1+_vec4_0;\n_vec4_1 = _vec4_array_128_3[gl_InstanceID];\n_vec4_0=p3d_ModelViewProjectionMatrix*_vec4_0;\ncol = _vec4_1;\nuv = p3d_MultiTexCoord0;\ngl_Position = _vec4_0;\n}",
    "fragment": "#version 450\n\nin vec2 uv;\nuniform sampler2D p3d_Texture0;\nin vec4 col;\nout vec4 p3d_FragColor;\n\nvoid main(){\nvec4 _vec4_0=texture(p3d_Texture0,uv);\n_vec4_0=col*_vec4_0;\np3d_FragColor = _vec4_0;\n}"
}

class InstancedCurve(InstancedEntity):

    main_group:InstancedGroup = None
    line_quality = 26

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
        InstancedCurve.main_group = InstancedGroup(
            parent = parent,
            default_class = InstancedCurve,
            model = Mesh(vertices = [(floor(i/2) / (InstancedCurve.line_quality - 1),  ((i + 1)%2) - 0.5, 0) for i in range(InstancedCurve.line_quality * 2)], 
                mode='tristrip', 
                static=False),
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