from ursina import *
from shader_instructions import DataTypeLayouts
from shader_node import ShaderNode

'''
Not actually a shader node, but helps set values for previewing changes in the shader.
'''

class PreviewShaderInputNode(ShaderNode):

    def __init__(self, input_list:dict, preview_entity:Entity, **kwargs):
        super().__init__(parent = camera.ui, draggable = False, **kwargs)

        self.shader_inputs = dict()
        self.preview_entity = preview_entity

        self.append_text('Shader Inputs')
        self.append_divider(3)
        self.append_text('Model', size = 0.8)
        self.append_divider()
        self.append_text('TODO: put in selector', size = 0.5)

        for k,v in input_list.items():
            data_type = v['data type']

            self.append_divider(3)
            self.append_text(k, size = 0.8)
            self.append_text(data_type, size = 0.5)
            self.append_divider()

            if data_type in DataTypeLayouts.keys():
                self.shader_inputs.update({
                    k : {
                        'data_type' : data_type,
                        'inputs' : [self.append_value_input(k2, v2, on_change = self.update_shader_input, on_change_att = str(k)) for k2,v2 in DataTypeLayouts[data_type].items()]
                    }
                })
            else:
                self.append_text('TODO: put in selector', size = 0.5)

        self.ui_back = self.build_back()
        
        self.x = window.left.x + self.ui_build_width * 0.5 + self.ui_spacing
        
        max = window.bottom.y - self.ui_build_pos + self.ui_spacing * 2
        min = window.top.y - self.ui_spacing * 5
        if max > min:
            self.add_script(Scrollable(min = min, max = max))
        self.y = min

    def update_shader_input(self, name):
        data_type = self.shader_inputs[name]['data_type']
        inp = self.shader_inputs[name]['inputs']

        if data_type in DataTypeLayouts.keys():
            vals = ()

            for i in inp:
                vals += ((i[1].text == 'true') if data_type[0] == 'b' else float(i[1].text),)
                
            self.preview_entity.set_shader_input(name, vals)
