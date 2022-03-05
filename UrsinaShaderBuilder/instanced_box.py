from ursina import *
from Prefabs.instanced_entity import InstancedEntity, InstancedGroup

Box_Shader = {
    "vertex": "#version 450\n\nuniform vec4[128] scales;\nin vec4 p3d_Vertex;\nuniform vec4[128] positions;\nuniform vec4[128] colors;\nuniform mat4 p3d_ModelViewProjectionMatrix;\nout vec4 color;\nout vec4 gl_Position;\n\nvoid main(){\nvec4[128] _vec4_array_128_2 = colors;\nvec4[128] _vec4_array_128_1 = positions;\nvec4[128] _vec4_array_128_0 = scales;\nvec4 _vec4_0 = _vec4_array_128_0[gl_InstanceID];\nvec2 _vec2_0 = vec2(_vec4_0.xy);\nfloat _float_0 = _vec4_0.z;\nfloat _float_1 = _vec4_0.w;\nvec2 _vec2_1 = vec2(p3d_Vertex.xy);\nfloat _float_2 = p3d_Vertex.z;\nfloat _float_3 = p3d_Vertex.w;\nvec2 _vec2_2 = vec2(_float_0,_float_1);\nvec2 _vec2_3=sign(_vec2_1);\n_vec2_1=_vec2_2*_vec2_1;\n_vec2_3=_vec2_0*_vec2_3;\n_vec2_1=_vec2_3+_vec2_1;\n_vec4_0 = vec4(_vec2_1,_float_2,_float_3);\nvec4 _vec4_1 = _vec4_array_128_1[gl_InstanceID];\n_vec4_0=_vec4_1+_vec4_0;\n_vec4_1 = _vec4_array_128_2[gl_InstanceID];\n_vec4_0=p3d_ModelViewProjectionMatrix*_vec4_0;\ncolor = _vec4_1;\ngl_Position = _vec4_0;\n}",
    "fragment": "#version 450\n\nin vec4 color;\nout vec4 p3d_FragColor;\n\nvoid main(){\np3d_FragColor = color;\n}"
}

class InstancedBox(InstancedEntity):

    main_group:InstancedGroup = None

    def __init__(self, **kwargs):
        self.box_scale = (0.1, 0.1, 0.02, 0.02)
        self.relative_position = Vec4(0,0,0,0)

        super().__init__(**( {'parent' : camera.ui} | kwargs | {'collider' : None}))

        if 'collider' in kwargs:
            self.collider = BoxCollider(self, 
                size = ((self.box_scale[0] * 2 + self.box_scale[2]), (self.box_scale[1] * 2 + self.box_scale[3]), 0.001))
    
    def visible_test(self):
        e = self
        while e != None:
            if not hasattr(e, 'visible'):
                return True
            if not e.visible or not e.enabled:
                return False
            e = e.parent
        return True

    def update(self):
        if self.instance_group != None:
            np = self.get_position(self.instance_group)
            if self.relative_position.xyz != np:
                self.relative_position = Vec4(np, 0)

    def __setattr__(self, name, value):
        if name == 'visible' and self.instance_group != None:
            self.instance_group.update_value(self, 'box_scale', self.box_scale if value else (0,0,0,0))
        if name == 'collider' and value == 'box':
            value = BoxCollider(self, 
                size = ((self.box_scale[0] * 2 + self.box_scale[2]), (self.box_scale[1] * 2 + self.box_scale[3]), 0.001))
        return super().__setattr__(name, value)


    def init_group(parent):
        InstancedBox.main_group = InstancedGroup(
            parent = parent,
            default_class = InstancedBox,
            model = 'circle',
            shader_attributes = {
                'relative_position' : 'positions' ,
                'box_scale' : 'scales',
                'color' : 'colors'
            }, 
            max_count = 128,
            shader = Shader(vertex = Box_Shader['vertex'], fragment = Box_Shader['fragment'])
            )

    def update_visibility():
        p = InstancedBox.main_group
        while p != None:
            for e in p.entities:
                e.instance_group.update_value(e, 'box_scale', e.box_scale if e.visible_test() else (0,0,0,0))
            p = p.group_chain

if __name__ == '__main__':
    app = Ursina()

    InstancedBox.init_group(camera.ui)
    print(InstancedBox.main_group.parent)

    e = InstancedBox.main_group.new_entity(parent = camera.ui, color = color.green, position = Vec3(1,0,-1))
    e2 = InstancedBox.main_group.new_entity(parent = camera.ui, color = color.red, position = Vec3(1,0,0))
    
    e3 = InstancedBox.main_group.new_entity(parent = camera.ui, position = Vec3(0,0,0))
    InstancedBox.main_group.new_entity(parent = camera.ui, position = Vec3(random.uniform(-0.5,0.5),0.2,0))
    InstancedBox.main_group.new_entity(parent = camera.ui, position = Vec3(random.uniform(-0.5,0.5),0.3,0))
    InstancedBox.main_group.new_entity(parent = camera.ui, position = Vec3(random.uniform(-0.5,0.5),0.4,0))
    InstancedBox.main_group.new_entity(parent = camera.ui, position = Vec3(random.uniform(-0.5,0.5),0.5,0))

    def input(key):
        if key == 'space':
            InstancedBox.main_group.parent = camera.ui
        if key == 'left arrow':
            e.position = Vec3(e.x - 0.1, e.y, e.z)
        if key == 'right arrow':
            e.x += 0.1
            print(e.parent)

    app.run()