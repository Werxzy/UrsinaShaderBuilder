from shader_instructions import DataTypes
from shader_node import ShaderNode

'''
Node represents an input specified by the user
'''

class UserInputNode(ShaderNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ui_name = self.append_value_input('Name', 'var')

        self.ui_type = self.append_drop_down('Type', dict((v,v) for v in DataTypes), self.on_selected)
        
        self.ui_back = self.build_back()

        self.main_output = self.build_connector('', ['vec4'], True, 0.5)

    def on_selected(self, option):
        self.ui_type[1].text = option
        self.main_output.variable_type = [option]
        self.manager.destroy_menu()
        self.update_connections()
        

    def build_shader(self):
        v1 = 'in ' + self.ui_type[1].text + ' ' + self.ui_name[1].text + ';'
        self.manager.build_shader_append('inout', v1)
        self.main_output.set_build_variable(self.ui_name[1].text)

        
