from ursina import destroy
from shader_instructions import DataTypes
from shader_node import ShaderNode

'''
Node represents an input or output specified by the user
'''

class UserInOutNode(ShaderNode):

    array_options = {
        'Single Variable' : 0,
        'Array' : 1,
        '2D Array' : 2,
        '3D Array' : 3,
    }

    def __init__(self, name = 'var', data_type = '', isOutput = True, **kwargs):
        super().__init__(**kwargs)
        self.ui_build_width = 0.26
        # if this node is outputing a variable
        self.isOutput = isOutput

        self.ui_name = self.append_value_input('Name', 'var')
        self.ui_name[1].text = name
        self.ui_name[1].render()
        self.ui_type = self.append_drop_down('Type', dict((v,v) for v in DataTypes), self.on_selected)
        if data_type != '': self.ui_type[1].text = data_type
        if self.isOutput:
            self.ui_uniform = self.append_value_input('Uniform Input', 'bool')

        self.ui_is_array = self.append_drop_down('', UserInOutNode.array_options, on_select = self.on_array_change,
            set_to_key = True)
        
        self.build_back()
        self.ui_dimensions = []

        self.main_connector = self.build_connector('', [self.ui_type[1].text], isOutput, 0.5)

    def on_array_change(self, option, replace_vals = []):
        while len(self.ui_dimensions) > option:
            self.remove_ui_section(self.ui_dimensions.pop())

        for i in range(len(self.ui_dimensions), option):
            self.ui_dimensions.append(self.append_value_input('[]'*i + '['+ 'xyzw'[i] +']', 'uint', on_change = self.update_data_type))
            if i < len(replace_vals):
                self.ui_dimensions[i][1].text = replace_vals[i]
                self.ui_dimensions[i][1].render(False)

        self.build_back()

        self.update_data_type()

    def on_selected(self, option):
        self.main_connector.variable_type = [option]
        self.update_data_type()

    def update_data_type(self, var = 'required'):
        ind = self.main_connector.variable_type[0].find('[')
        if ind == -1:
            data_type = self.main_connector.variable_type[0]
        else:
            data_type = self.main_connector.variable_type[0][:ind]
        
        for ui in self.ui_dimensions:
            data_type += '[' + ui[1].text + ']'

        self.main_connector.variable_type = [data_type]
        if self.isOutput:
            self.update_connections()
        elif self.main_connector.any_connected():
            self.main_connector.connections[0].parent.update_connections()

    def build_shader(self):
        if self.isOutput:
            v1 = 'in ' if self.ui_uniform[1].text == 'false' else 'uniform '
            if v1 == 'uniform ':
                self.manager.build_shader_input_append(self.ui_type[1].text, self.ui_name[1].text)

            v_dec = self.ui_type[1].text
            for ui in self.ui_dimensions: v_dec += '[' + ui[1].text + ']'
            v_dec += ' ' + self.ui_name[1].text
            
            if len(self.ui_dimensions) > 0:
                v2 = self.main_connector.prepare_build_variable() + ' = ' + self.ui_name[1].text + ';'
                self.manager.build_shader_append('main', v2, False)
            else:
                self.main_connector.set_build_variable(self.ui_name[1].text)

            v1 += v_dec + ';'

        else:
            v1 = 'out ' + self.ui_type[1].text
            for ui in self.ui_dimensions: v1 += '[' + ui[1].text + ']'
            v1 += ' ' + self.ui_name[1].text + ';'

            v2 = self.ui_name[1].text + ' = ' + self.main_connector.get_build_variable() + ';'
            self.manager.build_shader_append('main', v2)

        self.manager.build_shader_append('inout', v1)


    def save(self):
        data = {'name' : self.ui_name[1].text, 'data type' : self.ui_type[1].text, 'is output' : self.isOutput}
        if self.isOutput: 
            data.update({'uniform' : self.ui_uniform[1].text})

        if len(self.ui_dimensions) > 0:
            data.update({'is array' : self.ui_is_array[1].text})

            sizes = []
            for ui in self.ui_dimensions:
                sizes.append(ui[1].text)
            data.update({'array dimensions' : sizes})

        return data

    def load(manager, data):
        new_node = UserInOutNode(parent = manager, manager = manager, name = data['name'], data_type = data['data type'], isOutput = data['is output'])
        if new_node.isOutput:
            new_node.ui_uniform[1].set_value(data['uniform'] == 'true')

        if 'is array' in data.keys():
            new_node.ui_is_array[1].text = data['is array']
            new_node.on_array_change(UserInOutNode.array_options[data['is array']], data['array dimensions'])

        return new_node
        
