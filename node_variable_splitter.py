from ursina import destroy
from shader_node import ShaderNode

'''
Node that allows splitting and merging of values 
'''

class VariableSplitterNode(ShaderNode):

    versions = {
        'vec4' : ['float', 'float', 'float', 'float'],
        'vec3' : ['float', 'float', 'float'],
        'vec2' : ['float', 'float'],
        
        'mat4' : ['vec4', 'vec4', 'vec4', 'vec4'],
        'mat3' : ['vec3', 'vec3', 'vec3'],
        'mat2' : ['vec2', 'vec2'],

        'ivec4' : ['int', 'int', 'int', 'int'],
        'ivec3' : ['int', 'int', 'int'],
        'ivec2' : ['int', 'int'],
        
        'uvec4' : ['uint', 'uint', 'uint', 'uint'],
        'uvec3' : ['uint', 'uint', 'uint'],
        'uvec2' : ['uint', 'uint'],

        'bvec4' : ['bool', 'bool', 'bool', 'bool'],
        'bvec3' : ['bool', 'bool', 'bool'],
        'bvec2' : ['bool', 'bool'],
    }

    defaults = {
        'float' : '0.0',
        'int' : '0',
        'uint' : '0',
        'bool' : 'false',
        'vec2' : 'vec2(0,0)',
        'vec3' : 'vec3(0,0,0)',
        'vec4' : 'vec4(0,0,0,0)',
    }

    def __init__(self, data_type = '', merge = False, **kwargs):
        super().__init__(**kwargs)

        self.ui_name = self.append_text('Split/Merge', size = 0.8)

        self.div = self.append_divider()

        self.ui_type = self.append_drop_down('Type', dict((v,v) for v in VariableSplitterNode.versions), self.menu_select)
        if data_type != '': self.ui_type[1].text = data_type

        self.ui_merge = self.append_value_input('Merge', 'bool', on_change = self.rebuild_connections)
        self.ui_back = self.build_back()
        self.built = False

        self.rebuild_connections()

    def menu_select(self, option):
        self.rebuild_connections()

    def rebuild_connections(self, val='required'):
        if self.built:
            for i in self.inputs:
                i.disconnect_all()
                destroy(i)
            for o in self.outputs:
                o.disconnect_all()
                destroy(o)
            self.inputs.clear()
            self.outputs.clear()
        
        data_type = self.ui_type[1].text
        inout = self.ui_merge[1].text == 'false'

        i = 0.5
        self.build_connector(data_type, [data_type], not inout, i)
        
        for j,v in enumerate(VariableSplitterNode.versions[data_type]):
            self.build_connector('xyzw'[j], [v], inout, i, True)
            i += 1   

        self.built = True

    def build_shader(self):
        if self.ui_merge[1].text == 'false':
            v = self.inputs[0].get_build_variable()
            t = self.outputs[0].get_variable_type()

            for i,o in enumerate(self.outputs):
                if not o.any_connected(): continue

                v2 = o.prepare_build_variable()
                comp = ['[0]', '[1]', '[2]', '[3]'] if t.startswith('mat') else ['.x', '.y', '.z', '.w'] 
                    
                inst = v2 + ' = ' + v + comp[i] + ';'
                self.manager.build_shader_append('main', inst)

        else:
            v = self.outputs[0].prepare_build_variable()
            t = self.outputs[0].get_variable_type()
            inst = v + ' = ' + t + '('

            for i,inp in enumerate(self.inputs):
                if i > 0:  inst += ','
                inst += inp.get_build_variable() if inp.any_connected() else VariableSplitterNode.defaults[inp.get_variable_type()]

            inst += ');'
            self.manager.build_shader_append('main', inst)

    
    def save(self):
        return {'data type' : self.ui_type[1].text, 'merge' : self.ui_merge[1].text}

    def load(manager, data):
        new_node = VariableSplitterNode(parent = manager, manager = manager, data_type = data['data type'])
        new_node.ui_merge[1].set_value(data['merge'] == 'true')

        return new_node