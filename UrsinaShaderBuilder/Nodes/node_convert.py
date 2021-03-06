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
        'mat2','mat3','mat4',
        'mat2x3','mat2x4','mat3x2','mat3x4','mat4x2','mat4x3',
    ]

    sub_types = {
        'i' : 'int',
        'u' : 'uint',
    }

    def __init__(self, start_from = 'vec3', start_to = 'vec4', **kwargs):
        super().__init__(**kwargs)

        self.built = False

        self.append_text('Convert', size = 0.8)
        self.append_divider()

        self.ui_from = self.append_drop_down('From', dict([(v,v) for v in ConvertNode.allowed_types]), self.rebuild_connections, start_value = start_from)
        self.ui_to = self.append_drop_down('To', dict([(v,v) for v in ConvertNode.allowed_types]), self.rebuild_connections, start_value = start_to)

        self.build_back()

        self.rebuild_connections(start_from)

    def rebuild_connections(self, val:str):
        if self.built:
            for i in self.inputs:
                destroy(i)
            for o in self.outputs:
                destroy(o)
            self.inputs.clear()
            self.outputs.clear()
        
        type_from = self.ui_from[1].text
        type_to = self.ui_to[1].text

        if val.startswith('mat'):
            if self.check_field(self.ui_from[1], True, 'mat4'): return
            if self.check_field(self.ui_to[1], True, 'mat3'): return
        else:
            if self.check_field(self.ui_from[1], False, 'vec3'): return
            if self.check_field(self.ui_to[1], False, 'vec4'): return

        from_count = ConvertNode.component_count(type_from)
        to_count = ConvertNode.component_count(type_to)

        self.build_connector(type_from, [type_from], False, 0.5)
        self.build_connector(type_to, [type_to], True, 0.5)

        inout = from_count < to_count

        sub_type = ConvertNode.get_sub_type(type_from if inout else type_to)
        i = 1.5
        for j in range(min(from_count, to_count), max(from_count, to_count)):
            self.build_connector(sub_type, [sub_type], not inout, i, True)
            i += 1   

        self.built = True


    def check_field(self, field, is_mat, replacement):
        if field.text.startswith('mat') != is_mat:
            field.text = replacement
            self.rebuild_connections(replacement)
            return True
        return False

    def component_count(data_type:str):
        if data_type.startswith('mat'): return 1
        try: return int(data_type[-1])
        except: return 1

    def get_sub_type(data_type):
        if data_type[0] in ConvertNode.sub_types.keys():
            return ConvertNode.sub_types[data_type[0]]
        return 'float'

    
    def build_shader(self):
        type_from = self.ui_from[1].text
        type_to = self.ui_to[1].text

        from_count = ConvertNode.component_count(type_from)
        to_count = ConvertNode.component_count(type_to)

        inst = f'{self.outputs[0].prepare_build_variable()} = {type_to}('
        inst_extra = []

        if from_count <= to_count:
            for i,inp in enumerate(self.inputs):
                if i > 0: inst += ','
                inst += inp.get_build_variable() if inp.any_connected() else '0'
        else:
            in_var = self.inputs[0].get_build_variable()
            inst += in_var
            if from_count > 1:
                inst += '.xyzw'[:(to_count + 1)]
            for i in range(1, len(self.outputs)):
                if self.outputs[i].any_connected():
                    vo = self.outputs[i].prepare_build_variable()
                    inst_extra.append(f'{vo} = {in_var}.{"xyzw"[i + to_count - 1]};')

        inst += ');'
        self.manager.build_shader_append('main', inst)
        for i in inst_extra:
            self.manager.build_shader_append('main', i)

    def save(self):
        return {'from data type' : self.ui_from[1].text, 'to data type' : self.ui_to[1].text}

    def load(manager, data):
        return ConvertNode(parent = manager, manager = manager, start_from = data['from data type'], start_to = data['to data type'])