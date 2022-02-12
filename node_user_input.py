from re import S
from ursina import destroy
from shader_node import ShaderNode

'''
Node represents an input specified by the user
'''

class UserInputNode(ShaderNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ui_name = self.append_value_input('Name', 'var')

        self.ui_type = self.append_drop_down('Type', {'float':'float', 'vec2':'vec2', 'vec3':'vec3'}, self.on_selected)
        
        self.ui_back = self.build_back()

        self.main_output = self.build_connector('', ['vec4'], True, 0.157)

    def on_selected(self, option):
        self.ui_type[1].text = option
        self.main_output.variable_type = [option]
        destroy(self.manager.node_menu)
        self.update_connections()
        

    # def build_shader(self):
    #     v1 = 'out ' + self.inputs[0].get_variable_type() + ' ' + self.variable_name + ';'
    #     v2 = self.variable_name + ' = ' + self.inputs[0].get_build_variable() + ';'

    #     self.manager.build_shader_append('inout', v1)
    #     self.manager.build_shader_append('main', v2)
