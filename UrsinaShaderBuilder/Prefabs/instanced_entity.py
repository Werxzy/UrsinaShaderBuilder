from ursina import *

class InstancedEntity(Entity):

    def __init__(self, **kwargs):
        self.instance_group:InstancedGroup = None
        super().__init__(**kwargs)

    # Watches if any of the known attributes are being changed, then notifies the group entity.
    def __setattr__(self, name, value):       
        if hasattr(self, 'instance_group') and self.instance_group != None and name in self.instance_group.shader_attributes:
            self.instance_group.update_value(self, name, value)
        return super().__setattr__(name, value)
        
    # Remove self from the group entity when destroyed.
    def on_destroy(self):
        if self.instance_group != None:
            self.instance_group.remove(self)

    # Notify the group entity that a value has changed.
    def update_value(self, name):
        self.instance_group.update_value(self, name)


class InstancedGroup(Entity):

    def __init__(self, shader_attributes:dict[str, str] = {}, ursina_shader_file:dict = None, **kwargs):
        self.entities:list[InstancedEntity] = []
        self.shader_attributes = shader_attributes
        self.values = dict((v, []) for v in shader_attributes.keys())
        self.max_count = 256
        self.group_chain:InstancedGroup = None
        
        self.any_updated = True
        self.count_update = True
        self.to_update = set(shader_attributes.keys())

        self.default_class:type = InstancedEntity
        self.default_kwargs:dict[str] = {}

        self.org_kwargs = kwargs

        super().__init__(**kwargs)

        # not sure what to do with the bounding box
        from panda3d.core import BoundingBox
        node = self.node()       
        node.setBounds(BoundingBox(Vec3(-100,-100,-100), Vec3(100,100,100)))
        node.setFinal(True)

        assert self.max_count > 0

    def update(self):
        # Updates the number of instances of the model/shader
        if self.count_update:
            self.count_update = False
            self.setInstanceCount(len(self.entities))
            self.visible = len(self.entities) > 0

        # Updates any changes of the shader attributes.
        if self.any_updated:
            self.any_updated = False
            for k in self.to_update:
                self.set_shader_input(self.shader_attributes[k], self.values[k] if len(self.entities) > 0 else [0])
            self.to_update.clear()

    # Creates a new entity for the group.
    def new_entity(self, **kwargs) -> InstancedEntity:
        e = self.default_class(**(self.default_kwargs | kwargs))
        self.append(e)
        return e

    # Adds an entity to the list and notifies that shader attributes need to be updated.
    # If the number of entities reaches the max count, then a new group is created with the same settings.
    def append(self, entity:InstancedEntity):
        if len(self.entities) == self.max_count:
            if self.group_chain == None:
                self.group_chain = InstancedGroup(
                    shader_attributes = self.shader_attributes,
                    **(self.org_kwargs | {
                        'parent' : self, 
                        'position' : (0,0,0), 
                        'scale' : 1, 
                        'rotation' : (0,0,0),
                        'max_count' : self.max_count,
                        'default_class' : self.default_class,
                        'default_kwargs' : self.default_kwargs
                    }))
            self.group_chain.append(entity)
            return

        self.entities.append(entity)
        entity.instance_group = self
        
        for k in self.shader_attributes:
            self.values[k].append(getattr(entity, k))
        
        self.to_update.update(self.shader_attributes.keys())
        self.count_update = True
        self.any_updated = True

    # Adds an entity to the list and notifies that shader attributes need to be updated.
    def remove(self, entity:InstancedEntity):
        i = self.entities.index(entity)
        entity.instance_group = None
        
        for k in self.shader_attributes:
            self.values[k].pop(i)
        self.entities.pop(i)

        self.to_update.update(self.shader_attributes.keys())
        self.count_update = True
        self.any_updated = True

    # sets a value and notifies that the specific shader attribute needs to be updated.
    def update_value(self, entity, name, value = None):
        i = self.entities.index(entity)
        
        if value == None:
            value = getattr(entity, name)

        if self.values[name][i] != value:
            self.values[name][i] = value
            self.any_updated = True
            self.to_update.add(name)

if __name__ == '__main__':
    app = Ursina(vsync=False)

    instancing_shader=Shader(language=Shader.GLSL, vertex='''#version 140
    uniform mat4 p3d_ModelViewProjectionMatrix;
    in vec4 p3d_Vertex;
    in vec2 p3d_MultiTexCoord0;
    in vec3 p3d_Normal;
    out vec2 uv;
    out vec4 color;
    out vec3 normal;
    uniform vec3 positions[254];
    uniform vec4 rotations[254];
    uniform vec3 scales[254];
    uniform vec4 colors[254];
    void main() {
        vec3 v = p3d_Vertex.xyz * scales[gl_InstanceID];
        vec4 q = rotations[gl_InstanceID];
        v = v + 2.0 * cross(q.xyz, cross(q.xyz, v) + q.w * v);
        gl_Position = p3d_ModelViewProjectionMatrix * (vec4(v + positions[gl_InstanceID], 1.));
        normal = p3d_Normal + 2.0 * cross(q.xyz, cross(q.xyz, p3d_Normal) + q.w * p3d_Normal);
        uv = p3d_MultiTexCoord0;
        color = colors[gl_InstanceID];
    }
    ''',

    fragment='''
    #version 140
    uniform sampler2D p3d_Texture0;

    in vec2 uv;
    in vec4 color;
    in vec3 normal;
    out vec4 fragColor;
    void main() {
        vec4 color = texture(p3d_Texture0, uv) * color;
        color.rgb *= max(dot(normalize(vec3(1,1,1)), normalize(normal)), 0.2);
        fragColor = color.rgba;
    }
    ''')

    instEntity = InstancedGroup(
        model = 'cube',
        shader_attributes = {
            'position' : 'positions' ,
            'quaternion' : 'rotations' ,
            'scale' : 'scales' ,
            'color' : 'colors' 
        },
        max_count = 254,
        shader = instancing_shader)

    e = InstancedEntity()
    instEntity.append(e)
    e.rotation_x
    for i in range(200):
        instEntity.new_entity(x = random.uniform(-4,4), 
                y = random.uniform(-4,4),
                z = random.uniform(1,4),
                rotation_x = random.uniform(0,360),
                rotation_y = random.uniform(0,360),
                rotation_z = random.uniform(0,360),
                color = color.hsv(random.uniform(0,360), random.uniform(0,1), random.uniform(0,1), 1))

    def input(key):
        if key == 'left arrow':
            e.position = Vec3(e.x - 1, e.y, e.z)
        if key == 'right arrow':
            e.x += 1
            # 'position' isn't the variable being changed, so we tell the entity it needs to be updated for the group
            e.update_value('position')

    EditorCamera()

    app.run()