from shader_instructions import DataTypes
from shader_node import ShaderNode

'''
Node represents an input or output specified by the user
'''

class UserInOutNode(ShaderNode):

    def __init__(self, name = 'var', data_type = '', isOutput = True, **kwargs):
        super().__init__(**kwargs)
        self.ui_build_width = 0.26
        # if this node is outputing a variable
        self.isOutput = isOutput

        self.ui_name = self.append_value_input('Name', name)
        self.ui_type = self.append_drop_down('Type', dict((v,v) for v in DataTypes), self.on_selected)
        if data_type != '': self.ui_type[1].text = data_type
        if self.isOutput:
            self.ui_uniform = self.append_value_input('Uniform Input', 'bool')
        
        self.ui_back = self.build_back()

        self.main_connector = self.build_connector('', [self.ui_type[1].text], isOutput, 0.5)

    def on_selected(self, option):
        self.ui_type[1].text = option
        self.main_connector.variable_type = [option]
        self.manager.destroy_menu()
        if self.isOutput:
            self.update_connections()
        elif self.main_connector.any_connected():
            self.main_connector.connections[0].parent.update_connections()

    def build_shader(self):
        if self.isOutput:
            v1 = 'in '
            if self.isOutput:
                v1 = v1 if self.ui_uniform[1].text == 'false' else 'uniform '
            v1 += self.ui_type[1].text + ' ' + self.ui_name[1].text + ';'
            self.main_connector.set_build_variable(self.ui_name[1].text)

        else:
            v1 = 'out ' + self.ui_type[1].text + ' ' + self.ui_name[1].text + ';'
            v2 = self.ui_name[1].text + ' = ' + self.main_connector.get_build_variable() + ';'
            self.manager.build_shader_append('main', v2)

        self.manager.build_shader_append('inout', v1)

    def save(self):
        data = {'name' : self.ui_name[1].text, 'data type' : self.ui_type[1].text, 'is output' : self.isOutput}
        if self.isOutput: data.update({'uniform' : self.ui_uniform[1].text})

        return data

    def load(manager, data):
        new_node = UserInOutNode(parent = manager, manager = manager, name = data['name'], data_type = data['data type'], dataisOutput = data['is output'])
        if new_node.isOutput:
            new_node.ui_uniform[1].set_value(data['uniform'])

        return new_node
        
