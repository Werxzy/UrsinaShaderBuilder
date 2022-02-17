from ursina import destroy
from shader_node import ShaderNode

'''
Node that allows easily converting variables.

Excess components will be considered the same type of their respective side.
'''

class ConvertNode(ShaderNode):

    allowed_types = [
        'float', 'vec2', 'vec3', 'vec4',
        'int', 'ivec2', 'ivec3', 'ivec4',
        'uint', 'uvec2', 'uvec3', 'uvec4',
        'bool', 'bvec2', 'bvec3', 'bvec4',
    ]

    sub_types = {
        'i' : 'int',
        'u' : 'uint',
        'b' : 'bool',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.built = False

        self.ui_from = self.append_drop_down('From', dict([(v,v) for v in ConvertNode.allowed_types]), self.on_select, start_value = 'vec3')
        self.ui_to = self.append_drop_down('To', dict([(v,v) for v in ConvertNode.allowed_types]), self.on_select, start_value = 'vec4')

        self.rebuild_connections()

    def on_select(self, option):
        self.rebuild_connections()

    def rebuild_connections(self):
        if self.built:
            for i in self.inputs:
                i.disconnect_all()
                destroy(i)
            for o in self.outputs:
                o.disconnect_all()
                destroy(o)
            self.inputs.clear()
            self.outputs.clear()
        
        type_from = self.ui_from[1].text
        type_to = self.ui_to[1].text

        from_count = ConvertNode.component_count(type_from)
        to_count = ConvertNode.component_count(type_to)

        self.build_connector(type_from, [type_from], False, 0.5)
        self.build_connector(type_to, [type_to], True, 0.5)

        inout = from_count < to_count

        sub_type = ConvertNode.get_sub_type(type_from if inout else type_to)
        i = 1.5
        for j in range(min(from_count, to_count), max(from_count, to_count)):
            self.build_connector('xyzw'[j], [sub_type], inout, i, True)
            i += 1   

        self.built = True


    def component_count(data_type):
        if isinstance(type(data_type[-1]), int):
            return int(data_type[-1])
        return 1

    def get_sub_type(data_type):
        if data_type[0] in ConvertNode.sub_types.keys():
            return ConvertNode.sub_types[data_type[0]]
        return 'float'

    
    def build_shader(self):
        pass
    
    def save(self):
        return {'from data type' : self.ui_from[1].text, 'to data type' : self.ui_to[1].text}

    def load(manager, data):
        pass