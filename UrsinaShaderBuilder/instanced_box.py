from ursina import *
from Prefabs.instanced_entity import InstancedEntity, InstancedGroup
from ExtraData.builtin_shaders import Box_Shader

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