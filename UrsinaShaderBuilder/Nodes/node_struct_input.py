from ursina import destroy
from shader_instructions import DataTypes
from shader_node import ShaderNode

'''
Node represents an input or output specified by the user
'''

class StructInputNode(ShaderNode):

    array_options = {
        'Single Variable' : 0,
        'Array' : 1,
        '2D Array' : 2,
        '3D Array' : 3,
    }

    current_structs = {
        'No Struct Selected' : None
    }

    def __init__(self, name = 'var', struct_type = None, **kwargs):
        super().__init__(**kwargs)
        self.ui_build_width = 0.26

        self.ui_name = self.append_value_input('Name', 'var')
        self.ui_name[1].text = name
        self.ui_name[1].render()
        self.ui_type = self.append_drop_down('Type', StructInputNode.current_structs, self.on_selected, start_value = struct_type)

        self.ui_is_array = self.append_drop_down('', StructInputNode.array_options, on_select = self.on_array_change,
            set_to_key = True)
        
        self.build_back()
        self.ui_dimensions = []

        self.main_connector = self.build_connector('', [self.ui_type[1].text], True, 0.5)

    def on_array_change(self, option, replace_vals = []):
        while len(self.ui_dimensions) > option:
            self.remove_ui_section(self.ui_dimensions.pop())

        for i in range(len(self.ui_dimensions), option):
            self.ui_dimensions.append(self.append_value_input(f"{'[]'*i}[{'xyzw'[i]}]", 'uint', on_change = self.update_data_type))
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
            data_type += f'[{ui[1].text}]'

        self.main_connector.variable_type = [data_type]
        self.update_connections()


    def build_shader(self):
        v1 = 'uniform '
        self.manager.build_shader_input_append(self.ui_type[1].text, self.ui_name[1].text)

        v_dec = self.ui_type[1].text
        for ui in self.ui_dimensions: v_dec += f'[{ui[1].text}]'
        v_dec += ' ' + self.ui_name[1].text
        
        if len(self.ui_dimensions) > 0:
            v2 = f'{self.main_connector.prepare_build_variable()} = {self.ui_name[1].text};'
            self.manager.build_shader_append('main', v2, False)
        else:
            self.main_connector.set_build_variable(self.ui_name[1].text)

        v1 += v_dec + ';'

        self.manager.build_shader_append('inout', v1)


    def save(self):
        data = {'name' : self.ui_name[1].text, 'struct type' : self.ui_type[1].text}

        if len(self.ui_dimensions) > 0:
            data.update({'is array' : self.ui_is_array[1].text})

            sizes = []
            for ui in self.ui_dimensions:
                sizes.append(ui[1].text)
            data.update({'array dimensions' : sizes})

        return data

    def load(manager, data):
        new_node = StructInputNode(parent = manager, manager = manager, name = data['name'], struct_type = 'struct type')

        if 'is array' in data.keys():
            new_node.ui_is_array[1].text = data['is array']
            new_node.on_array_change(StructInputNode.array_options[data['is array']], data['array dimensions'])

        return new_node
        
